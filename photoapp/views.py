from typing import Union

from django.http import HttpResponseRedirect, HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from photoapp.forms import PhotoForm, PhotoSearchForm
from photoapp.services import MentionUserService, PhotoService


def photos(request: HttpRequest) -> HttpResponse:
    """
    Display a queryset of :model:`photoapp.Photo`.
    """
    user = request.user
    search_form = PhotoSearchForm(data=request.GET)
    if search_form.is_valid() and search_form.changed_data:
        search_parameters = search_form.cleaned_data
    else:
        search_parameters = {}

    photos_queryset = PhotoService.filter_photos_by_search(user, search_parameters)
    return render(request, "photoapp/photos.html", {
        "search_form": search_form,
        "photos": photos_queryset,
    })


def photo_details(request: HttpRequest, photo_id: int) -> HttpResponse:
    """
    Display an individual :model:`photoapp.Photo`.
    """
    photo = PhotoService.get_photo_or_404(photo_id, request.user)
    return render(request, "photoapp/photo_details.html", {
        "photo": photo,
    })


def add_photo(request: HttpRequest) -> Union[HttpResponse, HttpResponseRedirect]:
    """
    Create an instance of :model:`photoapp.Photo` and related an instance of :model:`photoapp.MentionUser`
    """
    if request.method == "POST":
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.created_by = request.user
            photo.save()
            mention_users = form.cleaned_data.get("mention_users")
            for username in mention_users:
                mention_user = MentionUserService.get_or_create_mention_user(username)
                PhotoService.associate_photo_with_mention_user(photo, mention_user)
            return HttpResponseRedirect(reverse("photo_details", kwargs={'photo_id': photo.id}))
        else:
            return render(request, "photoapp/add_photo.html", {"form": form})
    return render(request, "photoapp/add_photo.html", {"form": PhotoForm()})


def mention_users_api(request):
    mention_usernames = {}
    username = request.GET.get("username")
    if username:
        mention_usernames = MentionUserService.filter_existing_mentioned_users(username, request.user)
    return JsonResponse(list(mention_usernames), safe=False)
