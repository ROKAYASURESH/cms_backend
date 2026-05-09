from django.urls import path
from .views import PermissionTypeAPIView, PermissionTypeUpdateAPIView, PermissionTypeDeleteAPIView

urlpatterns = [
    path('permission-types/', PermissionTypeAPIView.as_view(), name='permission-types'),
    path('permission-types/<int:pk>/', PermissionTypeUpdateAPIView.as_view(), name='permission-type-update'),
    path('permission-types/<int:pk>/delete/', PermissionTypeDeleteAPIView.as_view(), name='permission-type-delete'),
]
