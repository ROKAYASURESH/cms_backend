from django.urls import path
from .views import *

urlpatterns = [
    path('sidebar-menu/', SidebarMenuView.as_view(), name='sidebar-menu'),  # sidebar

    path('menus/', MenuAPIView.as_view(), name='menus-list'),  
    path('menus/<int:pk>/', MenuDetailAPIView.as_view(), name='menus-detail'),  
    path('menus/parents/', ParentMenuListView.as_view(), name='parent-menu-list'),
]
 