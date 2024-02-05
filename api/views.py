from .serializers import AuthTokenSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken as BaseObtainAuthToken
from user.serializers import UserDetailSerializer

class ObtainAuthToken(BaseObtainAuthToken):
    serializer_class = AuthTokenSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        self.delete_old_tokens(user)
        
        response = super().post(request,*args,**kwargs)
        
        context = {'request': request}
        user_serializer = UserDetailSerializer(user,context=context)
        user_data = user_serializer.data
        response.data['user'] = user_data
        return response

    def delete_old_tokens(self, user):
        Token.objects.filter(user=user).delete()
    
obtain_auth_token = ObtainAuthToken.as_view()