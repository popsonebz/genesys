from django.contrib.auth import login, authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import (CreateAPIView, UpdateAPIView, RetrieveDestroyAPIView, ListAPIView)
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from .serializers import (UserSerializer, LoginSerializer, ChangePasswordSerializer)
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import User
from .custompermissions import IsOwner
from rest_framework.viewsets import ModelViewSet


class UserCreateView(CreateAPIView):
     queryset = User.objects.all()
     serializer_class = UserSerializer
     permission_classes = (AllowAny, )
     authentication_classes = ()


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser, )


class UserRetrieveOrDeleteView(RetrieveDestroyAPIView):
    lookup_field = 'id'
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAdminUser,)

    #def get_permissions(self):


class ChangePasswordView(UpdateAPIView):
    #lookup_field = 'id'
    serializer_class = ChangePasswordSerializer
    queryset = User.objects.all()
    permission_classes = (IsOwner, IsAuthenticated)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_200_OK, data={"Password updated successfully !"})



class LoginView(CreateAPIView):
    serializer_class= LoginSerializer
    queryset=User.objects.all()
    permission_classes = (AllowAny,)

    error_messages = {
        'invalid': "Invalid username or password",
        'disabled': "Sorry, this account is suspended",
    }

    def _error_response(self, message_key):
        data = {
            'success': False,
            'message': self.error_messages[message_key],
            'user_id': None,
        }
        return data

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(self, username=email, password=password) #
        if user is not None:
            if user.is_active:
                login(request, user,)
                return Response(status=status.HTTP_200_OK)
            return self._error_response('disabled')
        print(self.error_messages)
        return Response(data=self._error_response('invalid'))
