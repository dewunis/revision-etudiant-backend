from rest_framework import serializers
from .models import Level,Degree,Cursus,SchoolSystem,Formation
        
class LevelListSerializer(serializers.ModelSerializer):
    class Meta :
        model = Level
        fields = ('pk','name')

class CursusListSerializer(serializers.ModelSerializer):
    class Meta :
        model = Cursus
        fields = ('pk','name')
        
class SchoolSystemListSerializer(serializers.ModelSerializer):
    class Meta :
        model = Cursus
        fields = ('pk','name')
        
class FormationListSerializer(serializers.ModelSerializer):
    class Meta :
        model = Formation
        fields = ('pk','name','full_name','short_name')
        