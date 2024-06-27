from django.test import TestCase
from accounts.models import User
from .models import FriendRequest, Friendship
from django.core.exceptions import ValidationError
from .functions import list_friends, list_pending_requests, is_friend


class FriendModelTest(TestCase):
    def setUp(self):
        User.objects.create_user(id=1, email="user1@example.com", password="123")
        User.objects.create_user(id=2, email="user2@example.com", password="123")
        User.objects.create_user(id=3, email="user3@example.com", password="123")

    def test_friend_request_unique(self):
        """Test that a friend request can't exist in both directions."""
        FriendRequest.objects.create(from_user_id=1, to_user_id=2)

        with self.assertRaises(ValidationError):
            FriendRequest.objects.create(from_user_id=1, to_user_id=2)

        with self.assertRaises(ValidationError):
            FriendRequest.objects.create(from_user_id=2, to_user_id=1)

    def test_friend_request_accept(self):
        """Test that accepting a request creates a friendship."""
        request = FriendRequest.objects.create(from_user_id=1, to_user_id=2)
        request.accept()

        self.assertTrue(Friendship.objects.filter(user1_id=1, user2_id=2).exists())

    def test_friend_request_reject(self):
        """Test that rejecting a request deletes it."""
        request = FriendRequest.objects.create(from_user_id=1, to_user_id=2)
        request.reject()

        self.assertFalse(
            FriendRequest.objects.filter(from_user_id=1, to_user_id=2).exists()
        )

    def test_list_friends(self):
        """Test that list_friends returns correct friends."""
        FriendRequest.objects.create(from_user_id=1, to_user_id=2).accept()
        FriendRequest.objects.create(from_user_id=3, to_user_id=1).accept()

        friends = list_friends(1)
        self.assertEqual(friends.count(), 2)
        self.assertIn(2, friends.values_list("id", flat=True))
        self.assertIn(3, friends.values_list("id", flat=True))

    def test_list_pending_requests(self):
        """Test that list_pending_requests returns correct requests."""
        FriendRequest.objects.create(from_user_id=2, to_user_id=1)
        requests = list_pending_requests(1)
        self.assertEqual(requests.count(), 1)
        self.assertEqual(requests.first().from_user.id, 2)

    def test_is_friend(self):
        """Test that is_friend correctly identifies friends."""
        FriendRequest.objects.create(from_user_id=1, to_user_id=2).accept()

        self.assertTrue(is_friend(1, 2))
        self.assertTrue(is_friend(2, 1))  # Order shouldn't matter
