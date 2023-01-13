from unittest.mock import patch

from django.test import SimpleTestCase

from photoapp.forms import UsersSetField


class UsersSetFieldTestCase(SimpleTestCase):
    FORM_PATH = 'photoapp.forms'

    @patch(f'{FORM_PATH}.UsersSetField.__init__')
    def test_to_python(self, form_patch):
        form_patch.return_value = None
        form_mock = UsersSetField()

        value_mock = "Test, test , , another_test,  greAt_TEst, TEST"

        result = form_mock.to_python(value_mock)

        self.assertEqual(result, {"test", "another_test", "great_test"})
