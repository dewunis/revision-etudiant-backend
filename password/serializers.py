from rest_framework import serializers
from .validators import validate_password
from user.models import User
from rest_framework import serializers
from django.utils.translation import gettext as _

class PasswordResetCreateCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    
class PasswordResetConfirmCodeSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)   
    
class PasswordResetSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    code = serializers.CharField(required=True)   
    password = serializers.CharField(required=True,validators=[validate_password])
    confirm_password = serializers.CharField(required=True)
    
    def validate_confirm_password(self,confirm_password):
        if confirm_password != self.initial_data.get('password'):
            raise serializers.ValidationError(_('Mot de passe non identique.'))