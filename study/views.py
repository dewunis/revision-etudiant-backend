from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Level,Degree,Cursus,SchoolSystem,Formation

from .serializers import (
    LevelListSerializer,
    CursusListSerializer,
    FormationListSerializer,
    SchoolSystemListSerializer,
)

class SchoolSystemListApiView(generics.ListAPIView):
    queryset = SchoolSystem.objects.all()
    serializer_class = SchoolSystemListSerializer
    permission_classes = [AllowAny]
    
school_sytem_list_api_view = SchoolSystemListApiView.as_view()

class LevelListApiView(generics.ListAPIView):
    queryset = Level.objects.all()
    serializer_class = LevelListSerializer
    permission_classes = [AllowAny]
    
level_list_api_view = LevelListApiView.as_view()

class CursusListApiView(generics.ListAPIView):
    queryset = Cursus.objects.all()
    serializer_class = CursusListSerializer
    permission_classes = [AllowAny]
    
cursus_list_api_view = CursusListApiView.as_view()

class FormationListApiView(generics.ListAPIView):
    queryset = Formation.objects.all()
    serializer_class = FormationListSerializer
    permission_classes = [AllowAny]
    
formation_list_api_view = FormationListApiView.as_view()