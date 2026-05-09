from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from django.utils import timezone
from administrator.users.models import UserRole
from administrator.roles.models import Roles
from django.contrib.auth.models import User
from .serializers import UserListSerializer, UserCRUDSerializer, UserSerializer
from utils.paginators import get_paginated_queryset
from django.db.models import Prefetch
from decorators.decorators import permission_required

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().prefetch_related('userrole_set__role')
    serializer_class = UserCRUDSerializer

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return UserListSerializer
        return UserCRUDSerializer

    # @permission_required("user", "Browse")
    def list(self, request, *args, **kwargs):
        try:
            users = self.get_queryset()

            # Filtering logic
            username_list = request.GET.getlist("username[]")
            last_name = request.GET.get("last_name", "")
            first_name = request.GET.get("first_name", "")
            is_active = request.GET.get("is_active", None)

            if username_list:
                users = users.filter(username__in=username_list)
            if last_name:
                users = users.filter(last_name__icontains=last_name)
            if first_name:
                users = users.filter(first_name__icontains=first_name)
            if is_active is not None:
                is_active = is_active.lower() == "true"
                users = users.filter(is_active=is_active)

            # Sorting logic
            sort_column = request.GET.get("sort_column", "id")
            sort_order = request.GET.get("sort_order", "asc")
            order_prefix = "" if sort_order == "asc" else "-"
            users = users.order_by(f"{order_prefix}{sort_column}")

            # Pagination
            per_page = int(request.GET.get("per_page", 10))
            pagination_data = get_paginated_queryset(users, request, per_page=per_page)

            serializer = UserListSerializer(pagination_data["page_obj"], many=True)

            return Response(
                {
                    "user_roles": serializer.data,
                    "pagination": {
                        "total": pagination_data["total_items"],
                        "total_pages": pagination_data["total_pages"],
                        "current_page": pagination_data["current_page"],
                        "per_page": pagination_data["per_page"],
                        "page_range": pagination_data["page_range"],
                    },
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            raise APIException(f"Error fetching users: {str(e)}")

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({"message": "User deleted successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
