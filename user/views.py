from rest_framework import generics
from .models import User,Profil,Avatar
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from .permissions import IsOwnerOrReadOnly,IsProfileOwnerOrReadOnly
from api.mixins import IsStaffPermissionsMixin
from .validators import validate_foreign_keys

from .serializers import (
    UserListSerializer,
    UserCreateSerializer,
    UserDetailSerializer,
    UserDestroySerializer,
    UserUpdateSerializer,
    AvatarListSerializer,
    ProfilCreateSerializer,
    ProfilDetailSerializer,
)

class UserListApiView(IsStaffPermissionsMixin,generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer

user_list_api_view = UserListApiView.as_view()

class AvatarListApiView(generics.ListAPIView):
    queryset = Avatar.objects.all()
    serializer_class = AvatarListSerializer
    permission_classes = [AllowAny]
    
avatar_list_api_view = AvatarListApiView.as_view()

class UserCreateApiView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        context = {'request': request}
        user_serializer = UserDetailSerializer(user,context=context) 
        user_data = user_serializer.data
        
        response = {}
        response['token'] = user.auth_token.key
        response['user'] = user_data
        headers = self.get_success_headers(serializer.data)
        return Response(response, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self,serializer):
        user = serializer.save()
        validated_data = serializer.validated_data
        password = validated_data.get('password')
        user.set_password(password)
        user.save()
        Token.objects.create(user=user)
        return user

user_create_api_view = UserCreateApiView.as_view()

class UserDetailApiView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]
    
user_detail_api_view = UserDetailApiView.as_view()

class UserDestroyApiView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserDestroySerializer
    permission_classes = [IsOwnerOrReadOnly]

user_destroy_api_view = UserDestroyApiView.as_view()

class UserUpdateApiView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [IsOwnerOrReadOnly]
    
    def update(self, request, *args, **kwargs):
        errors = validate_foreign_keys(request.data)
        errors_status = status.HTTP_400_BAD_REQUEST
        if errors :
            return Response(errors,status=errors_status)
        return super().update(request, *args, **kwargs)

user_update_api_view = UserUpdateApiView.as_view()

class ProfilCreateApiView(generics.CreateAPIView) :
    queryset = Profil.objects.all()
    serializer_class = ProfilCreateSerializer
    permission_classes = [IsProfileOwnerOrReadOnly,IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        errors = validate_foreign_keys(request.data)
        errors_status = status.HTTP_400_BAD_REQUEST
        if errors :
            return Response(errors,status=errors_status)
        return super().create(request, *args, **kwargs)
     
profil_create_api_view = ProfilCreateApiView.as_view()

class ProfilDetailApiView(generics.RetrieveAPIView) :
    queryset = Profil.objects.all()
    lookup_field = 'user_id'
    serializer_class = ProfilDetailSerializer
    permission_classes = [IsOwnerOrReadOnly,IsAuthenticated]
     
profil_detail_api_view = ProfilDetailApiView.as_view()