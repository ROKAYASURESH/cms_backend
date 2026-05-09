from django.db import models
from django.contrib.auth.models import User
from administrator.roles.models import Roles
# Create your models here.
class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Roles, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('user', 'role')
        db_table='userrole'
        
    def __str__(self):
        return f"{self.user.username} - {self.role.role_name}"