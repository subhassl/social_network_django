from django.db import models
from django.core.exceptions import ValidationError
from accounts.models import User


class FriendRequest(models.Model):
    from_user = models.ForeignKey(
        User, related_name="sent_requests", on_delete=models.CASCADE
    )
    to_user = models.ForeignKey(
        User, related_name="received_requests", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.from_user} - {self.to_user}"

    def save(self, *args, **kwargs):
        # Check if a friend request already exists between the two users in either direction.
        if self.__class__.objects.filter(
            (
                models.Q(from_user=self.from_user, to_user=self.to_user)
                | models.Q(from_user=self.to_user, to_user=self.from_user)
            )
            & ~models.Q(pk=self.pk)  # ignore if pk matches for udates.
        ).exists():
            raise ValidationError("A friend request already exists.")

        super().save(*args, **kwargs)

    def accept(self):
        self.accepted = True
        self.save()

        # Create a new friendship object. Always set the smaller user id to user1.
        Friendship.objects.get_or_create(
            user1_id=min(self.from_user.id, self.to_user.id),
            user2_id=max(self.from_user.id, self.to_user.id),
        )

    def reject(self):
        self.delete()


class Friendship(models.Model):
    # user1_id < uid2_id. To avoid duplicates, we always store the smaller user id as user1.
    user1 = models.ForeignKey(
        User, related_name="user1_friendships", on_delete=models.CASCADE
    )
    user2 = models.ForeignKey(
        User, related_name="user2_friendships", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user1} - {self.user2}"

    class Meta:
        unique_together = ("user1", "user2")
