from django.urls import path
from . import views

urlpatterns = [
    path('level',views.level_list_api_view),
    path('cursus',views.cursus_list_api_view),
    path('formation',views.formation_list_api_view),
    path('school-system',views.school_sytem_list_api_view),
]