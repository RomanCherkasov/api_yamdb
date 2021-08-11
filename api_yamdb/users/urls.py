from django.urls import include, path
from rest_framework import routers
from users.views import UsersViewSet

router = routers.DefaultRouter()
router.register(r'users', UsersViewSet)

urlpatterns = [
    path('v1/', include(router.urls))
]