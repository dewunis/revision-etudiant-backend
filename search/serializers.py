from rest_framework import serializers
from study.models import Course

class SearchCourseSerializer(serializers.ModelSerializer):
    class Meta :
        model = Course
        fields = ('pk','name','formation')