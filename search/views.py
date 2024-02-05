from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .serializers import SearchCourseSerializer
from study.models import Course


class SearchCourseApiView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = SearchCourseSerializer
    # permission_classes = [IsAuthenticated]
    
    # def search() :
    #     return  Course.objects.none()
    
    def get_queryset(self,*args,**kwargs):
        default_results = Course.objects.none()
        qs = super().get_queryset(*args,**kwargs)
        data = self.request.GET
        
        formation = data.get('formation')
        query = data.get('q')
    
        return qs.search(
            query=query,
            formation=formation,
        )
        
search_course_api_view = SearchCourseApiView.as_view()  