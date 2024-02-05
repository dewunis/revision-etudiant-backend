from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from phonenumber_field.serializerfields import PhoneNumberField
from django.utils.translation import gettext as _

from study.models import Cursus,Formation
from core.utils import get_media_absolute_url
from .models import User,Profil,Avatar
from .validators import validate_name,vaildate_formation_choice,validate_country

class UserListSerializer(serializers.ModelSerializer):
    class Meta :
        model = User
        fields = ('id','first_name','last_name','email','created_at')
  
     
class UserCreateSerializer(serializers.ModelSerializer):
    class Meta :
        model = User
        fields = ('first_name','last_name','email','password')
            
    last_name = serializers.CharField(validators=[validate_name],max_length=30)
    first_name = serializers.CharField(validators=[validate_name],max_length=30)
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all(),message=_('Cette adresse email existe déjà.'))],max_length=255)
   
        
class UserDetailSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField(read_only=True)
    
    class Meta :
        model = User
        fields = ('id','first_name','last_name','email','avatar_url','phone_number','created_at')
  
    def get_avatar_url(self, obj):
        if not obj.avatar:
            return None
        request = self.context.get('request') 
        absolute_uri = get_media_absolute_url(request)
        return f'{absolute_uri}{obj.avatar}'
 
        
class UserDestroySerializer(serializers.ModelSerializer):
    class Meta :
        model = User
        fileds = ('id')
 

class UserUpdateSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField(read_only=True)
    
    class Meta :
        model = User
        fields = ('avatar_id','avatar_url','first_name','last_name','email','phone_number')
        
    def get_avatar_url(self, obj):
        if not obj.avatar:
            return None
        request = self.context.get('request') 
        absolute_uri = get_media_absolute_url(request)
        return f'{absolute_uri}{obj.avatar}'
    
        
    last_name = serializers.CharField(validators=[validate_name],max_length=30)
    first_name = serializers.CharField(validators=[validate_name],max_length=30) 
    phone_number = PhoneNumberField(region="TG")  
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all(),message=_('Cette adresse email existe déjà.'))],max_length=255)
    avatar_id = serializers.CharField(required=False)

        
class ProfilDetailSerializer(serializers.ModelSerializer):
    formation_full_name = serializers.SerializerMethodField(read_only=True)
    formation_short_name = serializers.SerializerMethodField(read_only=True)
    
    class Meta :
        model = Profil
        fields = ('level','cursus','school_system','country','formation','formation_short_name','formation_full_name')
        depth = 1
        
    def get_formation_full_name(self, obj):
        return f"{obj.formation.full_name}"
    
    def get_formation_short_name(self, obj):
        return f"{obj.formation.short_name}"
        
class AvatarListSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True) 

    class Meta :
        model = Avatar
        fields = ('pk','url','short_url')
        
    def get_url(self, obj):
        if not obj.avatar:
            return None
        request = self.context.get('request') 
        absolute_uri = get_media_absolute_url(request)
        return f'{absolute_uri}{obj.avatar}'

        
class ProfilCreateSerializer(serializers.ModelSerializer):
    class Meta :
        model = Profil
        fields = ('user_id','level_id','cursus_id','school_system_id','formation_id','country')
        
    def validate(self,data):
        vaildate_formation_choice(data)
        return data        
    
    country = serializers.CharField(required=False,validators=[validate_country])
    formation_id = serializers.CharField(required=False)
    level_id = serializers.CharField(required=True)
    school_system_id = serializers.CharField(required=True)
    cursus_id = serializers.CharField(required=True)
    user_id = serializers.CharField(validators=[UniqueValidator(queryset=Profil.objects.all(),message=_('Ce profile étudiant existe déja.'))])