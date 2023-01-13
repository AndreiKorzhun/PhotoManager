from typing import Union

from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse

from photoManager.settings import LOGIN_URL, LOGIN_REDIRECT_URL
from users.forms import RegisterForm, LoginForm


def login_view(request: HttpRequest) -> Union[HttpResponse, HttpResponseRedirect]:
    """
    Render LoginForm and authenticate a user
    """
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return HttpResponseRedirect(reverse(LOGIN_REDIRECT_URL))
        return render(request, "users/login.html", {"form": form})
    return render(request, "users/login.html", {"form": LoginForm()})


def logout_view(request: HttpRequest) -> HttpResponseRedirect:
    """
    Log out user and redirect to login page
    """
    logout(request)
    return HttpResponseRedirect(reverse(LOGIN_URL))


def register(request: HttpRequest) -> Union[HttpResponse, HttpResponseRedirect]:
    """
    Render RegisterForm and create a new user
    """
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect(reverse(LOGIN_REDIRECT_URL))
        return render(request, "users/register.html", {"form": form})
    return render(request, "users/register.html", {"form": RegisterForm()})
