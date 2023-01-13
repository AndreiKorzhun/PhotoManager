from unittest.mock import patch, MagicMock, call

from django.test import SimpleTestCase

from photoapp.views import photos, photo_details, add_photo, mention_users_api


class PhotoAppViewsTestCase(SimpleTestCase):
    VIEW_PATH = 'photoapp.views'

    @patch(f'{VIEW_PATH}.render')
    @patch(f'{VIEW_PATH}.PhotoService.filter_photos_by_search')
    @patch(f'{VIEW_PATH}.PhotoSearchForm')
    def test_photos__form_is_valid(self, form_patch, filter_photos_patch, render_patch):
        request_mock = MagicMock()

        form_mock = MagicMock(changed_data=True)
        form_mock.is_valid.return_value = True
        form_patch.return_value = form_mock

        photos_mock = MagicMock()
        filter_photos_patch.return_value = photos_mock

        result = photos(request_mock)

        self.assertEqual(result, render_patch.return_value)
        form_patch.assert_called_once_with(data=request_mock.GET)
        form_mock.is_valid.assert_called_once_with()
        filter_photos_patch.assert_called_once_with(request_mock.user, form_mock.cleaned_data)
        render_patch.assert_called_once_with(request_mock, "photoapp/photos.html", {
            "search_form": form_mock,
            "photos": photos_mock,
        })

    @patch(f'{VIEW_PATH}.render')
    @patch(f'{VIEW_PATH}.PhotoService.filter_photos_by_search')
    @patch(f'{VIEW_PATH}.PhotoSearchForm')
    def test_photos__form_is_invalid(self, form_patch, filter_photos_patch, render_patch):
        request_mock = MagicMock()

        form_mock = MagicMock(changed_data=False)
        form_mock.is_valid.return_value = False
        form_patch.return_value = form_mock

        photos_mock = MagicMock()
        filter_photos_patch.return_value = photos_mock

        result = photos(request_mock)

        self.assertEqual(result, render_patch.return_value)
        form_patch.assert_called_once_with(data=request_mock.GET)
        form_mock.is_valid.assert_called_once_with()
        filter_photos_patch.assert_called_once_with(request_mock.user, {})
        render_patch.assert_called_once_with(request_mock, "photoapp/photos.html", {
            "search_form": form_mock,
            "photos": photos_mock,
        })

    @patch(f'{VIEW_PATH}.render')
    @patch(f'{VIEW_PATH}.PhotoService.get_photo_or_404')
    def test_photo_details(self, get_photo_patch, render_patch):
        request_mock = MagicMock()
        photo_id_mock = MagicMock()

        result = photo_details(request_mock, photo_id_mock)

        self.assertEqual(result, render_patch.return_value)
        get_photo_patch.assert_called_once_with(photo_id_mock, request_mock.user)
        render_patch.assert_called_once_with(request_mock, "photoapp/photo_details.html", {
            "photo": get_photo_patch.return_value,
        })

    @patch(f'{VIEW_PATH}.render')
    @patch(f'{VIEW_PATH}.PhotoForm')
    def test_add_photo__get(self, form_patch, render_patch):
        request_mock = MagicMock(method="GET")

        result = add_photo(request_mock)

        self.assertEqual(result, render_patch.return_value)
        form_patch.assert_called_once_with()
        render_patch.assert_called_once_with(request_mock, "photoapp/add_photo.html", {
            "form": form_patch.return_value,
        })

    @patch(f'{VIEW_PATH}.HttpResponseRedirect')
    @patch(f'{VIEW_PATH}.reverse')
    @patch(f'{VIEW_PATH}.PhotoService.associate_photo_with_mention_user')
    @patch(f'{VIEW_PATH}.MentionUserService.get_or_create_mention_user')
    @patch(f'{VIEW_PATH}.PhotoForm')
    def test_add_photo__form_is_valid(self, form_patch, get_or_create_patch, photo_service_patch,
                                      reverse_patch, http_redirect_patch):
        request_mock = MagicMock(method="POST")

        form_mock = MagicMock()
        form_mock.is_valid.return_value = True
        mention_users_mock = {"user1", "user2"}
        form_mock.cleaned_data = {"mention_users": mention_users_mock}
        form_patch.return_value = form_mock

        photo_mock = MagicMock()
        form_mock.save.return_value = photo_mock

        mention_user_mock = MagicMock()
        get_or_create_patch.return_value = mention_user_mock
        reverse_mock = MagicMock()
        reverse_patch.return_value = reverse_mock

        result = add_photo(request_mock)

        self.assertEqual(result, http_redirect_patch.return_value)
        form_patch.assert_called_once_with(request_mock.POST, request_mock.FILES)
        form_mock.is_valid.assert_called_once_with()
        form_mock.save.assert_called_once_with(commit=False)
        photo_mock.save.assert_called_once_with()
        self.assertEqual(get_or_create_patch.call_count, len(mention_users_mock))
        get_or_create_patch.assert_has_calls([call("user1"), call("user2")], any_order=True)
        self.assertEqual(photo_service_patch.call_count, len(mention_users_mock))
        photo_service_patch.assert_called_with(photo_mock, get_or_create_patch.return_value)

    @patch(f'{VIEW_PATH}.render')
    @patch(f'{VIEW_PATH}.PhotoForm')
    def test_add_photo__form_is_invalid(self, form_patch, render_patch):
        request_mock = MagicMock(method="POST")

        form_mock = MagicMock()
        form_mock.is_valid.return_value = False
        form_patch.return_value = form_mock

        result = add_photo(request_mock)

        self.assertEqual(result, render_patch.return_value)
        form_patch.assert_called_once_with(request_mock.POST, request_mock.FILES)
        form_mock.is_valid.assert_called_once_with()
        render_patch.assert_called_once_with(request_mock, "photoapp/add_photo.html", {
            "form": form_mock,
        })

    @patch(f'{VIEW_PATH}.JsonResponse')
    @patch(f'{VIEW_PATH}.MentionUserService.filter_existing_mentioned_users')
    def test_mention_users_api__has_username(self, filter_users_patch, json_response_patch):
        request_mock = MagicMock()
        request_mock.GET = {"username": MagicMock()}

        result = mention_users_api(request_mock)

        self.assertEqual(result, json_response_patch.return_value)
        filter_users_patch.assert_called_once_with(request_mock.GET["username"], request_mock.user)
        json_response_patch.assert_called_once_with(list(filter_users_patch.return_value), safe=False)

    @patch(f'{VIEW_PATH}.JsonResponse')
    def test_mention_users_api__empty_username(self, json_response_patch):
        request_mock = MagicMock()
        request_mock.GET = {"username": ""}

        result = mention_users_api(request_mock)

        self.assertEqual(result, json_response_patch.return_value)
        json_response_patch.assert_called_once_with(list({}), safe=False)
