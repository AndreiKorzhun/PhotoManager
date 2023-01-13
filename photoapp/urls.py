from django.urls import path

from photoapp.views import photos, photo_details, add_photo, mention_users_api

urlpatterns = [
    path('', photos, name="photos"),
    path('photo/<int:photo_id>', photo_details, name="photo_details"),
    path('add_photo/', add_photo, name="add_photo"),
    path('json/', mention_users_api, name="mention_users_api"),
]
