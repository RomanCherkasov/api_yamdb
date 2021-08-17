from django.urls import include, path
from rest_framework import routers
from users.views import RegistrationsAPIView, TokenSenderAPIView, UserViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
auth_url = [path('auth/signup/', RegistrationsAPIView.as_view()),
            path('auth/token/', TokenSenderAPIView.as_view())]

app_name = 'users'
urlpatterns = [
    path('v1/', include(auth_url)),
    path('v1/', include(router.urls))
]
