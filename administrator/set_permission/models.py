from django.db import models
from administrator.roles.models import Roles
from administrator.permission_type.models import PermissionType
from administrator.menus.models import Menu
class SetPermission(models.Model):
    role = models.ForeignKey(Roles, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    permission_type = models.ForeignKey(PermissionType, on_delete=models.CASCADE)
    has_permission = models.BooleanField(default=False)

    class Meta:
        unique_together = ['role', 'menu', 'permission_type']