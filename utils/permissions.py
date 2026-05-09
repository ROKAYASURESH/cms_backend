from django.core.cache import cache
from django.contrib.auth.models import User
from collections import defaultdict
from administrator.set_permission.models import SetPermission
from administrator.roles.models import Roles

def has_permission(user: User, menu, permission_type):
    # cache_key = 'role_menu_permissions'
    # role_permissions = cache.get(cache_key)
    
    if user.is_superuser:
        return True
    
    roles = Roles.objects.filter(userrole__user=user)
    # if role_permissions is None:
    role_permissions = defaultdict(lambda: defaultdict(list))
    permissions = SetPermission.objects.select_related('role', 'menu', 'permission_type').all()
    
    for permission in permissions:
        role_name = permission.role.role_name
        menu_name = permission.menu.slug
        permission_type_name = permission.permission_type.name
        
        role_permissions[role_name][menu_name].append(permission_type_name)
        
        # cache.set(cache_key, dict(role_permissions), timeout=60 * 60 * 24)
    
    for role in roles:
        if role.role_name in role_permissions and permission_type in role_permissions[role.role_name][menu]:
            return True
    
    return False