from rest_framework import serializers
from .models import SetPermission
from administrator.roles.models import Roles
from administrator.menus.models import Menu
from administrator.permission_type.models import PermissionType
class MenuSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = ['id', 'title', 'parent', 'children']

    def get_children(self, obj):
        children = Menu.objects.filter(parent=obj)
        return MenuSerializer(children, many=True).data

class PermissionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermissionType
        fields = ['id', 'name']

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = ['id', 'role_name']

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SetPermission
        fields = ['role', 'menu', 'permission_type', 'has_permission']
