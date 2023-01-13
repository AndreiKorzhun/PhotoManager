from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from photoapp.models import Photo, MentionUser
from users.models import User


class PhotoService:
    @staticmethod
    def filter_photos_by_search(user: User, search_parameters: dict) -> QuerySet[Photo]:
        """
        Filtering a queryset of photos by the search parameters.
        """
        photos = Photo.objects.filter(created_by=user)
        if search_parameters:
            geolocation = search_parameters.get("geolocation")
            created_at = search_parameters.get("created_at")
            mention_user = search_parameters.get("mention_user")
            if geolocation:
                photos = photos.filter(geolocation__contains=geolocation)
            if created_at:
                photos = photos.filter(created_at__date=created_at)
            if mention_user:
                photos = photos.filter(mention_users__username__istartswith=mention_user)
        return photos

    @staticmethod
    def get_photo_or_404(photo_id: int, user: User) -> Photo:
        """
        Gets a Photo instance or raise a Http404 exception if the object does not exist.
        """
        return get_object_or_404(Photo, pk=photo_id, created_by=user)

    @staticmethod
    def associate_photo_with_mention_user(photo: Photo, mention_user: MentionUser) -> None:
        """
        Associate an Article instance with a Publication.
        """
        photo.mention_users.add(mention_user)
