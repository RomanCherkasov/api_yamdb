from django.urls import include, path

from users.views import RegistrationsAPIView, TokenSenderAPIView
app_name = 'users'
urlpatterns = [
    path('v1/auth/signup/', RegistrationsAPIView.as_view()),
    path('v1/auth/token/', TokenSenderAPIView.as_view())
]
