from django.urls import path
from .views import *

urlpatterns = [
    path('permission-typess/', PermissionTypeListView.as_view(), name='permission-types'),
    path('permissions/<int:role_id>/', PermissionsByRoleView.as_view(), name='permissions-by-role'),
    path('permissions/', PermissionsByRoleView.as_view(), name='permissions'),
]