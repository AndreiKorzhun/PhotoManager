from django.db.models import QuerySet

from photoapp.models import MentionUser
from users.models import User


class MentionUserService:
    @staticmethod
    def get_or_create_mention_user(username: str) -> MentionUser:
        """
        Gets, if exists, or creates a MentionUser object.
        """
        mention_user, _ = MentionUser.objects.get_or_create(username=username)
        return mention_user

    @staticmethod
    def filter_existing_mentioned_users(username: str, user: User) -> QuerySet[dict]:
        """
        Filter the existing mentioned users who are mentioned in the photos of the current user.
        """
        return MentionUser.objects.filter(
            username__istartswith=username, user_photos__created_by=user).distinct().values("username")
