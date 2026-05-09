from rest_framework import serializers
from .models import PermissionType

class PermissionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermissionType
        fields = '__all__'