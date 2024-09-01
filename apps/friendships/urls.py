from django.urls import path
from .views import (
    SendFriendRequestView,
    AcceptFriendRequestView,
    RejectFriendRequestView,
    ListFriendsView,
    ListPendingFriendRequestsView,
)

urlpatterns = [
    path(
        "friends/requests/send/",
        SendFriendRequestView.as_view(),
        name="send-friend-request",
    ),
    path(
        "friends/requests/accept/",
        AcceptFriendRequestView.as_view(),
        name="accept-friend-request",
    ),
    path(
        "friends/requests/reject/",
        RejectFriendRequestView.as_view(),
        name="reject-friend-request",
    ),
    path(
        "friends/list/",
        ListFriendsView.as_view(),
        name="list-friends",
    ),
    path(
        "friends/requests/pending/",
        ListPendingFriendRequestsView.as_view(),
        name="list-pending-friend-requests",
    ),
]
