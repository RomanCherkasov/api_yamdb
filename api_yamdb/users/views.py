from rest_framework import status, viewsets
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from django_filters.rest_framework import DjangoFilterBackend
from users.models import User
from rest_framework.decorators import action
from users.serializers import RegistrationSerializer, UsersSerializer
from users.permissions import AdminOnly


class RegistrationsAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data
        if request.data.get(
                'username'
        ) and request.data.get('username') == 'me':
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            'username': serializer.data.get('username'),
            'email': serializer.data.get('email')}
        confirm_code = default_token_generator.make_token(User.objects.last())
        print(confirm_code)
        return Response(data, status=status.HTTP_200_OK)


class TokenSenderAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        if request.data.get(
                'username'
        ) and request.data.get('confirmation_code'):
            user = get_object_or_404(User,
                                     username=request.data.get('username'))
            confirmation_code = request.data.get('confirmation_code')
            if default_token_generator.check_token(user, confirmation_code):
                return Response({
                    'token': str(AccessToken.for_user(user))
                }, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (AdminOnly,)
    filter_backends = (DjangoFilterBackend,)
    fillterset_fields = ('username',)

    def get_queryset(self):
        return self.queryset

    def get_object(self):
        username = self.kwargs.get('pk')
        user = get_object_or_404(User, username=username)
        return user

    @action(detail=False, permission_classes=(IsAuthenticated,),
            methods=['patch', 'get', 'post'])
    def me(self, request):
        print(request.method)
        if request.method == 'GET':
            user = get_object_or_404(User, username=self.request._user)
            data = {"username": user.username,
                    "email": user.email,
                    "role": user.role,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "bio": user.bio}
            return Response(data)

        if request.method == 'PATCH':
            print(request.data)
            user = get_object_or_404(User, username=self.request._user)
            print(user.email)
            data = request.data
            if user.role == 'user' and request.data.get('role') != 'user':
                data._mutable = True
                data.update({'role': 'user'})
                data._mutable = False
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=False)
            serializer.update(user, data)
            print(user)
            return Response(data, status=status.HTTP_200_OK)
