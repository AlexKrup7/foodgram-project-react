from rest_framework import status
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.pagination import LimitPageNumberPagination

from .models import Subscribe, User
from .serializers import SubscriptionListSerializer, SubscriptionSerializer


class FollowView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        data = {'user': request.user.id, 'following': id}
        serializer = SubscriptionSerializer(
            data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        user = request.user
        following = get_object_or_404(User, id=id)
        subscribe = get_object_or_404(
            Subscribe, user=user, following=following)
        subscribe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FollowListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = LimitPageNumberPagination

    def get(self, request):
        user = request.user
        queryset = User.objects.filter(following__user=user)
        page = self.paginate_queryset(queryset)
        serializer = SubscriptionListSerializer(
            page, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
