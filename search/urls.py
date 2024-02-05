from django.urls import path
from . import views

urlpatterns = [
   path('course',views.search_course_api_view,name='search-course'),
]