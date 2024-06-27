from rest_framework.throttling import UserRateThrottle


class SendFriendRequestThrottle(UserRateThrottle):
    rate = "3/min"
