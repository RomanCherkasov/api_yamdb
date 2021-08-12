from django.urls import include, path
from rest_framework import routers

from users.views import RegistrationsAPIView, TokenSenderAPIView, UserViewSet, MeViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'users/<str:me>', MeViewSet)

# router.register(r'users/(?P<username>\d+)', UserViewSet)
app_name = 'users'
urlpatterns = [
    path('v1/auth/signup/', RegistrationsAPIView.as_view()),
    path('v1/auth/token/', TokenSenderAPIView.as_view()),
    path('v1/', include(router.urls))
]