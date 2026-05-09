from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from utils.dropdown import DropdownView

api_patterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("", include("administrator.menus.urls")),
    path("", include("administrator.roles.urls")),
    path("", include("administrator.permission_type.urls")),
    path("", include("administrator.set_permission.urls")),
    path("", include("administrator.users.urls")),
    path("dropdown/", DropdownView.as_view(), name="dropdown"),

]

urlpatterns = [
    path("api/", include(api_patterns)),
    path("admin/", admin.site.urls),
]