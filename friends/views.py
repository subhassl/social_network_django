import logging
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.models import User
from accounts.serializers import UserSerializer
from .models import FriendRequest, Friendship
from .throttles import SendFriendRequestThrottle
from .functions import (
    list_friends,
    list_pending_requests,
)
from .serializers import PendingFriendRequestSerializer, FriendRequestSerializer


class ListFriendsView(APIView):
    def get(self, request):
        friends = list_friends(request.user.id)
        serializer = UserSerializer(friends, many=True)
        return Response({"friends": serializer.data}, status=status.HTTP_200_OK)


class ListPendingFriendRequestsView(APIView):
    def get(self, request):
        pending_requests = list_pending_requests(request.user.id)
        serializer = PendingFriendRequestSerializer(pending_requests, many=True)

        return Response(
            {"pending_requests": serializer.data}, status=status.HTTP_200_OK
        )


class SendFriendRequestView(APIView):
    throttle_classes = [SendFriendRequestThrottle]

    def post(self, request):
        logger = logging.getLogger(__name__)

        try:
            serializer = FriendRequestSerializer(
                data={
                    "from_user": request.user.id,
                    "to_user": request.data.get("to_user_id"),
                }
            )

            if serializer.is_valid():
                serializer.save()
                logger.info(
                    f"Sent friend request from User with ID {request.user.id} to User with ID {request.data.get('to_user_id')}"
                )
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            logger.warning(f"invalid request: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AcceptFriendRequestView(APIView):
    def post(self, request):
        logger = logging.getLogger(__name__)

        to_user = request.user
        from_user_id = request.data.get("from_user_id")

        try:
            friend_request = FriendRequest.objects.get(
                from_user_id=from_user_id, to_user=to_user, accepted=False
            )
            friend_request.accept()
            logger.info(
                f"Accepted friend request of User with ID {from_user_id} sent to User with ID {to_user.id}."
            )

            return Response(
                {"message": "Friend request accepted."},
                status=status.HTTP_200_OK,
            )

        except FriendRequest.DoesNotExist:
            logger.warning(
                f"invalid request: Friend request from User with ID {from_user_id} to User ID {to_user.id} does not exist or has already been accepted."
            )
            return Response(
                {"error": "Friend request not found or already accepted."},
                status=status.HTTP_404_NOT_FOUND,
            )


class RejectFriendRequestView(APIView):
    def post(self, request):
        logger = logging.getLogger(__name__)

        to_user = request.user
        from_user_id = request.data.get("from_user_id")

        try:
            friend_request = FriendRequest.objects.get(
                from_user_id=from_user_id, to_user=to_user, accepted=False
            )
            friend_request.reject()
            logger.info(
                f"Rejected friend request of User with ID {from_user_id} sent to User with ID {to_user.id}."
            )

            return Response(
                {"message": "Friend request rejected."},
                status=status.HTTP_200_OK,
            )

        except FriendRequest.DoesNotExist:
            logger.warning(
                f"invalid request: Friend request from User with ID {from_user_id} to User ID {to_user.id} does not exist or has already been accepted."
            )
            return Response(
                {"error": "Friend request not found or already accepted."},
                status=status.HTTP_404_NOT_FOUND,
            )
