# views.py
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Friendship
from .serializers import FriendRequestSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class SearchUsersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        search_query = request.query_params.get("search", "").strip().lower()
        if not search_query:
            return Response(
                {"error": "Search query is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check if the search query matches an exact email.
        users = User.objects.filter(
            Q(email__iexact=search_query) | Q(name__icontains=search_query)
        ).distinct()
        users_list = [
            {"id": user.id, "name": user.name, "email": user.email} for user in users
        ]

        return Response(users_list[:10], status=status.HTTP_200_OK)


class SendFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        sender = request.user
        receiver_email = request.data.get("receiver_email")

        if not receiver_email:
            return Response(
                {"error": "Receiver email is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            receiver = User.objects.get(email__iexact=receiver_email)
        except User.DoesNotExist:
            return Response(
                {"error": "User with the given email does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if sender.id == receiver.id:
            return Response(
                {"error": "You cannot send a friend request to yourself"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        existing_friendship = Friendship.objects.filter(
            Q(from_user=sender, to_user=receiver)
            | Q(from_user=receiver, to_user=sender)
        ).first()

        if existing_friendship:
            if existing_friendship.status == "accepted":
                return Response(
                    {"error": "You are already friends with this user"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            elif existing_friendship.from_user == sender:
                return Response(
                    {"error": "Friend request already sent"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                return Response(
                    {"error": "This user has already sent you a friend request"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        one_minute_ago = timezone.now() - timedelta(minutes=1)
        recent_requests = Friendship.objects.filter(
            from_user=sender, created_at__gte=one_minute_ago
        ).count()

        if recent_requests >= 3:
            return Response(
                {
                    "error": "You cannot send more than 3 friend requests within a minute"
                },
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )

        friend_request = Friendship(from_user=sender, to_user=receiver)
        friend_request.save()

        serializer = FriendRequestSerializer(friend_request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AcceptFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        sender_email = request.data.get("sender_email")
        if not sender_email:
            return Response(
                {"error": "Sender email is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            friend_request = Friendship.objects.get(
                to_user=request.user,
                from_user__email__iexact=sender_email,
                status="pending",
            )
        except Friendship.DoesNotExist:
            return Response(
                {"error": "Friend request not found"}, status=status.HTTP_404_NOT_FOUND
            )

        friend_request.status = "accepted"
        friend_request.save()

        return Response(
            {"message": "Friend request accepted"}, status=status.HTTP_200_OK
        )


class RejectFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        sender_email = request.data.get("sender_email")
        if not sender_email:
            return Response(
                {"error": "Sender email is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            friend_request = Friendship.objects.get(
                to_user=request.user,
                from_user__email__iexact=sender_email,
                status="pending",
            )
        except Friendship.DoesNotExist:
            return Response(
                {"error": "Friend request not found"}, status=status.HTTP_404_NOT_FOUND
            )

        friend_request.status = "rejected"
        friend_request.save()

        return Response(
            {"message": "Friend request rejected"}, status=status.HTTP_200_OK
        )


class ListFriendsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        friends = Friendship.objects.filter(
            Q(from_user=request.user, status="accepted")
            | Q(to_user=request.user, status="accepted")
        ).select_related("from_user", "to_user")

        friends_list = [
            {
                "id": (
                    friend.to_user.id
                    if friend.from_user == request.user
                    else friend.from_user.id
                ),
                "name": (
                    friend.to_user.name
                    if friend.from_user == request.user
                    else friend.from_user.name
                ),
                "email": (
                    friend.to_user.email
                    if friend.from_user == request.user
                    else friend.from_user.email
                ),
            }
            for friend in friends
        ]
        return Response(friends_list, status=status.HTTP_200_OK)


class ListPendingFriendRequestsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        pending_requests = Friendship.objects.filter(
            to_user=request.user, status="pending"
        ).select_related("from_user")

        pending_list = [
            {
                "id": req.id,
                "sender_id": req.from_user.id,
                "sender_name": req.from_user.name,
                "sender_email": req.from_user.email,
                "timestamp": req.created_at,
            }
            for req in pending_requests
        ]
        return Response(pending_list, status=status.HTTP_200_OK)
