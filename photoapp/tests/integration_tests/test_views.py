from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse

from photoapp.models import Photo, MentionUser
from users.models import User


class PhotoAppViewsTestCase(TestCase):
    VIEW_PATH = "photoapp.views"
    test_password = "1234%^&*Qwer"
    test_image_patch = "/test_photo.jpg"

    def setUp(self):
        self.user = User.objects.create_user(username="test_username", password=self.test_password)

        self.mention_user = MentionUser.objects.create(username="Test_Mention_User")
        self.photo = Photo.objects.create(
            image=self.test_image_patch,
            created_by=self.user,
            geolocation="test_geolocation",
        )
        self.photo.mention_users.add(self.mention_user)

        self.photos_url = reverse("photos")
        self.photo_details_url = reverse("photo_details", kwargs={"photo_id": self.photo.id})
        self.add_photo_url = reverse("add_photo")

        self.client = Client()
        self.client.login(username=self.user.username, password=self.test_password)

    def test_photos(self):
        response = self.client.get(self.photos_url, {"geolocation": "test_geo"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "photoapp/photos.html")

    def test_photo_details(self):
        response = self.client.get(self.photo_details_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "photoapp/photo_details.html")

    def test_add_photo__get(self):
        response = self.client.get(self.add_photo_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "photoapp/add_photo.html")

    def test_add_photo__form_is_valid(self):
        response = self.client.post(
            self.add_photo_url,
            {
                "image": SimpleUploadedFile(
                    name='test_image.jpg',
                    content=open(f"media/{self.test_image_patch}", 'rb').read(),
                    content_type='image/jpeg',
                ),
                "description": "Test Description",
                "mention_users": "Test, Test_Mention_User",
            },
        )
        self.assertEqual(response.status_code, 302)
        test_photo = Photo.objects.last()
        self.assertEqual(response.url, reverse("photo_details", kwargs={"photo_id": test_photo.id}))
        test_user = MentionUser.objects.filter(username="Test").first()
        self.assertTrue(test_user in test_photo.mention_users.all())

    def test_add_photo__form_is_invalid(self):
        response = self.client.post(self.add_photo_url, data={
            "description": "Test Description",
            "mention_users": "Test_Mention_User, Test",
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "photoapp/add_photo.html")
