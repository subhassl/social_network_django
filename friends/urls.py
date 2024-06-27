from django.urls import path
from . import views


urlpatterns = [
    path("friends/", views.ListFriendsView.as_view()),
    path("pending-requests/", views.ListPendingFriendRequestsView.as_view()),
    path("send-friend-request/", views.SendFriendRequestView.as_view()),
    path("accept-friend-request/", views.AcceptFriendRequestView.as_view()),
    path("reject-friend-request/", views.RejectFriendRequestView.as_view()),
]
