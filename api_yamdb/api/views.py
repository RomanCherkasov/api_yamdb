from api.permissions import IsAdminOrReadOnly
from api.serializers import (CategoriesSerializer, GenresSerializer,
                             TitlesSerializer)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from reviews.models import Categories, Genres, Titles


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('categories', 'genres', 'name', 'year')


class CategoriesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [IsAdminOrReadOnly]


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = [IsAdminOrReadOnly]
