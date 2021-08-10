from rest_framework.viewsets import GenericViewSet
from api.views import (CategoriesViewSet, GenresViewSet, TitlesSerializer, CategoriesSerializer, GenresSerializer, TitlesViewSet)
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'titles', TitlesViewSet)
router.register(r'categories', CategoriesViewSet)
router.register(r'genres', GenresViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),


]