from unittest.mock import patch, MagicMock

from django.test import SimpleTestCase

from photoapp.services import PhotoService


class PhotoServiceTestCase(SimpleTestCase):
    SERVICES_PATH = "photoapp.services.photo_service"

    @patch(f"{SERVICES_PATH}.Photo.objects.filter")
    def test_filter_photos_by_search__empty_parameters(self, filter_photo_patch):
        user_mock = MagicMock()
        search_parameters = {}

        result = PhotoService.filter_photos_by_search(user_mock, search_parameters)

        self.assertEqual(result, filter_photo_patch.return_value)
        filter_photo_patch.assert_called_once_with(created_by=user_mock)

    @patch(f"{SERVICES_PATH}.Photo.objects.filter")
    def test_filter_photos_by_search__with_parameters(self, filter_photo_patch):
        user_mock = MagicMock()
        search_parameters = {"geolocation": MagicMock(), "created_at": MagicMock(), "mention_user": MagicMock()}

        filter_photo_mock = MagicMock()
        filter_photo_patch.return_value = filter_photo_mock

        result = PhotoService.filter_photos_by_search(user_mock, search_parameters)

        self.assertEqual(result, filter_photo_mock.filter.return_value.filter.return_value.filter.return_value)
        filter_photo_patch.assert_called_once_with(created_by=user_mock)
        filter_photo_mock.filter.assert_called_once_with(geolocation__contains=search_parameters["geolocation"])
        filter_photo_mock.filter.return_value.filter.assert_called_once_with(
            created_at__date=search_parameters["created_at"])
        filter_photo_mock.filter.return_value.filter.return_value.filter.assert_called_once_with(
            mention_users__username__istartswith=search_parameters["mention_user"])

    @patch(f"{SERVICES_PATH}.Photo")
    @patch(f"{SERVICES_PATH}.get_object_or_404")
    def test_get_photo_or_404(self, get_obj_patch, photo_model_patch):
        photo_id_mock = MagicMock()
        user_mock = MagicMock()

        result = PhotoService.get_photo_or_404(photo_id_mock, user_mock)

        self.assertEqual(result, get_obj_patch.return_value)
        get_obj_patch.assert_called_once_with(photo_model_patch, pk=photo_id_mock, created_by=user_mock)

    def test_associate_photo_with_mention_user(self):
        photo_mock = MagicMock()
        mention_user_mock = MagicMock()

        PhotoService.associate_photo_with_mention_user(photo_mock, mention_user_mock)

        photo_mock.mention_users.add.assert_called_once_with(mention_user_mock)
