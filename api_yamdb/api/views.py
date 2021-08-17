from api.permissions import FullAcessOrReadOnlyPermission, IsAdminOrReadOnly
from api.serializers import (CategoriesSerializer, CommentSerializer,
                             GenresSerializer, ReviewSerializer,
                             TitlesSerializer, TitlesWriteSerializer)
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.exceptions import ValidationError
from reviews.models import Categories, Genres, Review, Title

from .filters import TitleFilter


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitlesSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitlesSerializer
        return TitlesWriteSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CreateListDeleteViewSet(mixins.CreateModelMixin,
                              mixins.ListModelMixin,
                              mixins.DestroyModelMixin,
                              viewsets.GenericViewSet):
    pass


class CategoriesViewSet(CreateListDeleteViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenresViewSet(CreateListDeleteViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [FullAcessOrReadOnlyPermission]

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        if title.reviews.filter(author=self.request.user).exists():
            raise ValidationError(
                'Пользователь может оставить '
                'только один отзыв на произведение!'
            )
        serializer.save(author=self.request.user, title_id=title.id)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [FullAcessOrReadOnlyPermission]

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review.objects.select_related('title'),
            title__id=self.kwargs.get('title_id'),
            pk=self.kwargs.get('review_id')
        )
        serializer.save(author=self.request.user, review_id=review.id)

    def get_queryset(self):
        review = get_object_or_404(
            Review.objects.select_related('title'),
            title__id=self.kwargs.get('title_id'),
            pk=self.kwargs.get('review_id')
        )
        return review.comments.all()
