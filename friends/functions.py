from accounts.models import User
from .models import FriendRequest, Friendship
from django.db.models import Q, F


def list_friends(user_id):
    """list_friends returns the list of friends for the user."""

    return User.objects.filter(
        Q(user1_friendships__user2_id=user_id) | Q(user2_friendships__user1_id=user_id)
    )


def list_pending_requests(user_id):
    """list_pending_requests returns the list of pending friend requests for the user."""

    return (
        FriendRequest.objects.filter(to_user_id=user_id)
        .filter(accepted=False)
        .select_related("from_user")
    )


def is_friend(user1_id, user2_id):
    """is_friend returns if two users are friends are not."""

    user1_id, user2_id = min(user1_id, user2_id), max(user1_id, user2_id)
    return Friendship.objects.filter(user1_id=user1_id, user2_id=user2_id).exists()
