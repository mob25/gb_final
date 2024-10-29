from django.contrib.auth import get_user_model
from recipes.pagination import LimitNumberPagination
from recipes.serializers import FollowSerializer
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Follow
from .serializers import UserCreateSerializer, UserReadSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    pagination_class = LimitNumberPagination
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserReadSerializer
        return UserCreateSerializer

    @action(methods=['get', 'delete'], detail=True,
            permission_classes=[IsAuthenticated],
            url_path='subscribe')
    def subscribe(self, request, pk):
        author = get_object_or_404(User, id=pk)

        if request.method == 'GET':
            if Follow.objects.filter(author=author,
                                     user=request.user).exists():
                return Response({'errors': 'Вы уже подписаны'},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                follow = Follow.objects.create(
                    user=request.user, author=author)
                serializer = FollowSerializer(
                    follow, context={'request': request})
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
        else:
            if not Follow.objects.filter(author=author,
                                         user=request.user).exists():
                return Response(
                    {'errors': 'Вы не подписаны на данного пользователя'},
                    status=status.HTTP_400_BAD_REQUEST)
            else:
                follow = Follow.objects.filter(
                    user=request.user, author=author)
                if follow:
                    follow.delete()
                    return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=False,
            permission_classes=[IsAuthenticated], url_path='subscriptions')
    def subscriptions(self, request):
        queryset = Follow.objects.filter(user=request.user)
        page = self.paginate_queryset(queryset)
        serializer = FollowSerializer(page, many=True,
                                      context={'request': request})
        return self.get_paginated_response(serializer.data)

    @action(methods=['get'], detail=False,
            permission_classes=[IsAuthenticated], url_path='me')
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(data=serializer.data)

    @action(methods=['post'], detail=False,
            permission_classes=[IsAuthenticated], url_path='set_password')
    def set_password(self, request):
        request.user.set_password(request.data['new_password'])
        request.user.save()
        return Response(data=request.data, status=status.HTTP_201_CREATED)

    @action(detail=False, permission_classes=[AllowAny], methods=['post'])
    def logout(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
