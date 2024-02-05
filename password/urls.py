from django.urls import path,include
from . import views

urlpatterns = [
   path('reset',views.password_reset_api_view,name='reset'),
   path('reset-code',views.password_reset_create_code_api_view,name='reset_code'),
   path('reset-confirm-code',views.password_reset_confirm_code_api_view,name='reset_confirm_code'),
]
