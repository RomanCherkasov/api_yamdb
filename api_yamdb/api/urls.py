from api.views import CategoriesViewSet, GenresViewSet, TitlesViewSet
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'titles', TitlesViewSet)
router.register(r'categories', CategoriesViewSet)
router.register(r'genres', GenresViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),


]
