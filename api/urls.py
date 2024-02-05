from django.urls import path,include
from . import views

urlpatterns = [
   path('auth',views.obtain_auth_token),
   path('user/',include('user.urls')),
   path('study/',include('study.urls')),
   path('password/',include('password.urls')),
   path('search/',include('search.urls')), 
]