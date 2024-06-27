from rest_framework import serializers
from accounts.models import User
from accounts.serializers import UserSerializer
from .models import FriendRequest
from .functions import is_friend


class PendingFriendRequestSerializer(serializers.ModelSerializer):

    from_user = UserSerializer()

    class Meta:
        model = FriendRequest
        fields = ["from_user", "created_at"]


class FriendRequestSerializer(serializers.ModelSerializer):
    from_user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    to_user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        error_messages={
            "does_not_exist": "The provided user id does not exist.",
        },
    )

    class Meta:
        model = FriendRequest
        fields = ["from_user", "to_user", "created_at"]

    def validate(self, attrs):
        from_user = attrs.get("from_user")
        to_user = attrs.get("to_user")

        # Check if to_user is different from from_user
        if from_user == to_user:
            raise serializers.ValidationError(
                "You cannot send a friend request to yourself."
            )

        # Check if the users are friends already
        if is_friend(from_user.id, to_user.id):
            raise serializers.ValidationError("You are already friends with this user.")

        return attrs
