from django.urls import path
from .views import *
urlpatterns = [
    path('roles/', RoleAPIView.as_view(), name='roles-list-create'),  
   
    path('roles/<int:pk>/', RolesUpdateAPIView.as_view(), name='roles-update'),  # Update
    path('roles/<int:pk>/delete/', RolesDeleteAPIView.as_view(), name='roles-delete'),
]