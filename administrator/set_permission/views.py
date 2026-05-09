from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from administrator.set_permission.models import SetPermission
from administrator.permission_type.models import PermissionType
from administrator.set_permission.serializers import PermissionTypeSerializer, PermissionSerializer, MenuSerializer, RoleSerializer
from administrator.menus.models import Menu
from administrator.roles.models import Roles
from django.core.cache import cache
class RoleListView(APIView):
    def get(self, request):
        roles = Roles.objects.all()
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data)

class MenuListView(APIView):
    def get(self, request):
        menus = Menu.objects.filter(parent__isnull=True)
        serializer = MenuSerializer(menus, many=True)
        return Response(serializer.data)

class PermissionTypeListView(APIView):
    def get(self, request):
        types = PermissionType.objects.all()
        serializer = PermissionTypeSerializer(types, many=True)
        return Response(serializer.data)

class PermissionsByRoleView(APIView):
    def get(self, request, role_id):
        permissions = SetPermission.objects.filter(role_id=role_id)
        serializer = PermissionSerializer(permissions, many=True)
        return Response({"permissions": serializer.data})

    def post(self, request):
        cache.delete('role_menu_permissions')
        role_id = request.data.get('role_id')
        permissions = request.data.get('permissions')
        if not role_id or not permissions:
            return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

        # Clear existing permissions for the role
        SetPermission.objects.filter(role_id=role_id).delete()

        # Save new permissions
        for key, allowed in permissions.items():
            menu_id, permission_type_id = key.split('_')
        try:
            for key, allowed in permissions.items():
                menu_id, permission_type_id = key.split('_')
                if allowed:
                    SetPermission.objects.create(
                        role_id=role_id,
                        menu_id=menu_id,
                        permission_type_id=permission_type_id,
                        has_permission=allowed
                    )
            return Response({"message": "Permissions updated successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


