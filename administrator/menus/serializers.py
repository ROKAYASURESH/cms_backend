from rest_framework import serializers
from .models import Menu

class ChildMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['id', 'title']

class MenuSerializer(serializers.ModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(queryset=Menu.objects.all(), allow_null=True)
    parent_title = serializers.CharField(source='parent.title', read_only=True)

    children = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = '__all__'

    def get_children(self, menu):
        children = menu.children.all().order_by('position')
        return ChildMenuSerializer(children, many=True).data

class ParentMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['id', 'title']