from rest_framework import serializers
from django.contrib.auth.models import User
from administrator.roles.models import Roles
from administrator.users.models import UserRole
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = ['id', 'role_name']

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False,allow_null=True, allow_blank=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'is_active']

    def create(self, validated_data):
        """
        Handle user creation with hashed passwords.
        """
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)  
        user.save()
        return user

    def update(self, instance, validated_data):
        """
        Handle user update with hashed passwords.
        """
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)  
        instance.save()
        return instance


class UserListSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'roles']

    def get_roles(self, obj):
        return [
            {"id": role.role.id, "role_name": role.role.role_name}
            for role in obj.userrole_set.all()
        ]

class UserCRUDSerializer(serializers.ModelSerializer):
    """
    Serializer for creating/updating users with multiple roles.
    """
    roles = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(queryset=Roles.objects.all()),
        write_only=True,
        required=False
    )
    password = serializers.CharField(write_only=True, required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'is_active', 'roles']

    def validate_username(self, value):
        user = self.context.get('view').get_object() if self.instance else None
        if User.objects.exclude(pk=user.pk if user else None).filter(username=value).exists():
            raise ValidationError("A user with that username already exists.")
        return value

    def create(self, validated_data):
        roles_data = validated_data.pop('roles', [])
        password = validated_data.pop('password', None)
        
        user = User.objects.create(**validated_data)
        if password:
            user.set_password(password)
            user.save()

        # Associate roles
        for role in roles_data:
            UserRole.objects.create(user=user, role=role)
            
        return user

    def update(self, instance, validated_data):
        roles_data = validated_data.pop('roles', None)
        password = validated_data.pop('password', None)

        # Update user fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if password:
            instance.set_password(password)
        
        instance.save()

        # Update roles if provided
        if roles_data is not None:
            UserRole.objects.filter(user=instance).delete()
            for role in roles_data:
                UserRole.objects.create(user=instance, role=role)

        return instance
