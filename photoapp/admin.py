from django.contrib import admin
from django.forms import ModelForm, Textarea

from photoapp.models import Photo, MentionUser


class PhotoModelForm(ModelForm):
    """
    A form for creating a photo in the Django admin site.
    """
    class Meta:
        model = Photo
        fields = '__all__'
        widgets = {
            'description': Textarea(attrs={'rows': 5, 'cols': 80}),
        }


class PhotoModelAdmin(admin.ModelAdmin):
    """
    The representation of :model:`photoapp.Photo` in the admin interface.
    """
    form = PhotoModelForm


admin.site.register(Photo, PhotoModelAdmin)
admin.site.register(MentionUser)
