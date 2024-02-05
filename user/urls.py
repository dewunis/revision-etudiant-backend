from django.urls import path,include
from . import views

urlpatterns = [
   path('',views.user_list_api_view,name='user_list'),
   path('avatar',views.avatar_list_api_view,name='avatar_list'),
   path('create',views.user_create_api_view,name='user_create'),
   path('<int:pk>',views.user_detail_api_view,name='user_detail'),
   path('<int:pk>/destroy',views.user_destroy_api_view,name='user_destroy'),
   path('<int:pk>/update',views.user_update_api_view,name='user_update'),
   path('<int:user_id>/profil',views.profil_detail_api_view,name='profil_detail'),
   path('profil/create',views.profil_create_api_view,name='profil_create'),
]
