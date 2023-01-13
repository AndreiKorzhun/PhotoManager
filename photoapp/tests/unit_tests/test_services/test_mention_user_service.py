from unittest.mock import patch, MagicMock

from django.test import SimpleTestCase

from photoapp.services import MentionUserService


class MentionUserServiceTestCase(SimpleTestCase):
    SERVICES_PATH = "photoapp.services.mention_user_service"

    @patch(f"{SERVICES_PATH}.MentionUser.objects.get_or_create")
    def test_get_or_create_mention_user(self, get_object_patch):
        username_mock = MagicMock()

        mention_user_mock = MentionUserService()
        get_object_patch.return_value = (mention_user_mock, None)

        result = MentionUserService.get_or_create_mention_user(username_mock)

        self.assertEqual(result, mention_user_mock)
        get_object_patch.assert_called_once_with(username=username_mock)

    @patch(f"{SERVICES_PATH}.MentionUser.objects.filter")
    def test_filter_existing_mentioned_users(self, filter_patch):
        username_mock = MagicMock()
        user_mock = MagicMock()

        filter_mock = MagicMock()
        filter_patch.return_value = filter_mock

        result = MentionUserService.filter_existing_mentioned_users(username_mock, user_mock)

        self.assertEqual(result, filter_mock.distinct.return_value.values.return_value)
        filter_patch.assert_called_once_with(username__istartswith=username_mock, user_photos__created_by=user_mock)
        filter_mock.distinct.assert_called_once_with()
        filter_mock.distinct.return_value.values.assert_called_once_with("username")
