from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from users.models import User

from users.serializers import RegistrationSerializer


class RegistrationsAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data
        if request.data.get('username') and request.data.get('username') == 'me':
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            'username':serializer.data.get('username'),
            'email':serializer.data.get('email')}
        confirm_code = default_token_generator.make_token(User.objects.last())
        print(confirm_code)
        return Response(data, status=status.HTTP_200_OK)


class TokenSenderAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        if request.data.get('username') and request.data.get('confirmation_code'):
            user = get_object_or_404(User, username=request.data.get('username'))
            confirmation_code = request.data.get('confirmation_code')
            if default_token_generator.check_token(user, confirmation_code):
                return Response({
                    'token': str(AccessToken.for_user(user))
                }, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)