from django import forms
from django.forms import TextInput

from photoapp.models import Photo


class UsersSetField(forms.Field):
    def to_python(self, value):
        """
        Normalize data to a set of lowercase strings.

        Split value by comma, strip whitespace and converted to lowercase.

        >>> UsersSetField.to_python("A, a, B , , c")
        {"a", "b", "c"}

        :param value: comma-separated string
        :return: set of strings
        """
        if not value:
            return set()
        users_map_obj = map(str.strip, value.split(","))
        return set([item.lower() for item in users_map_obj if item])


class CustomDateInput(forms.DateInput):
    input_type = "date"


class PhotoForm(forms.ModelForm):
    """
    A form for creating a photo.
    """
    mention_users = UsersSetField(required=False, help_text="A comma-separated list of users.")

    class Meta:
        model = Photo
        fields = ["image", "description", "geolocation", "mention_users"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }


class PhotoSearchForm(forms.Form):
    """
    A form for filtering photo queryset.
    """
    geolocation = forms.CharField(required=False, max_length=100)
    created_at = forms.DateField(
        required=False,
        widget=CustomDateInput,
    )
    mention_user = forms.CharField(required=False, max_length=64, widget=TextInput(attrs={"autocomplete": "off"}))
