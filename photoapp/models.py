from django.db import models

from users.models import User


class LowercaseCharField(models.CharField):
    """
    Override CharField to convert string to lowercase before saving.
    """
    def to_python(self, value):
        """
        Convert string to lowercase.
        """
        value = super(LowercaseCharField, self).to_python(value)
        if isinstance(value, str):
            return value.lower()
        return value


class MentionUser(models.Model):
    """
    Stores a single mention user entry, related to :model:`photoapp.Photo`.
    """
    username = LowercaseCharField(max_length=400)

    def __str__(self):
        return self.username

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
        }


class Photo(models.Model):
    """
    Stores a single photo entry, related to :model:`users.User` and :model:`photoapp.MentionUser`.
    """
    image = models.ImageField(upload_to='photos/')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=400, blank=True, null=True)
    mention_users = models.ManyToManyField(MentionUser, blank=True, related_name="user_photos")
    geolocation = models.CharField(max_length=100, blank=True, null=True)
