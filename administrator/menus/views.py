
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from .models import Menu
from .serializers import MenuSerializer, ParentMenuSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException
from utils.paginators import get_paginated_queryset
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated 
from decorators.decorators import permission_required
from administrator.users.models import UserRole
from administrator.permission_type.models import PermissionType

# SideBar
class SidebarMenuView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.is_superuser:
            top_level_menus = Menu.objects.filter(parent__isnull=True).prefetch_related('children').order_by('position')
            
            def build_menu_hierarchy_admin(menu):
                children = menu.children.all().order_by('position')
                return {
                    'id': menu.id,
                    'title': menu.title,
                    'url': menu.url,
                    'icon': menu.icon,
                    'position': menu.position,
                    'children': [build_menu_hierarchy_admin(child) for child in children]
                }
            
            serialized_data = [build_menu_hierarchy_admin(menu) for menu in top_level_menus]
        else:
            user_roles = UserRole.objects.filter(user=user).values_list('role_id', flat=True)
            try:
                browse_permission = PermissionType.objects.get(name='Browse')
            except PermissionType.DoesNotExist:
                return Response({"error": "Browse permission type not found"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            top_level_menus = Menu.objects.filter(
                parent__isnull=True,
                setpermission__role_id__in=user_roles,
                setpermission__permission_type=browse_permission,
                setpermission__has_permission=True
            ).distinct().prefetch_related('children').order_by('position')

            def build_menu_hierarchy(menu):
                children = menu.children.filter(
                    setpermission__role_id__in=user_roles,
                    setpermission__permission_type=browse_permission,
                    setpermission__has_permission=True
                ).distinct().order_by('position')
                return {
                    'id': menu.id,
                    'title': menu.title,
                    'url': menu.url,
                    'icon': menu.icon,
                    'position': menu.position,
                    'children': [build_menu_hierarchy(child) for child in children]
                }

            serialized_data = [build_menu_hierarchy(menu) for menu in top_level_menus]

        return Response(serialized_data)
     


class MenuAPIView(APIView):
    @permission_required('menus', 'Browse')
    def get(self, request, *args, **kwargs):
        try:
            menus = Menu.objects.all()
            parent_id = request.GET.get("parent_id", None)
            parent_title= request.GET.get("parent_title", None)
            title= request.GET.getlist("title[]", None)
            search = request.GET.get("search", None)
            status_param = request.GET.get("status", None)
            icon = request.GET.get("icon", None)

            query = Q()
            if parent_id:
                query &= Q(parent__id=parent_id)
            if parent_title and parent_title != 'all':
                if parent_title == 'root':
                    query &= Q(parent__isnull=True)
                else:
                    query &= Q(parent__title=parent_title)
            if title:
                query &= Q(title__in=title)
            if search:
                query &= (Q(title__icontains=search) | Q(url__icontains=search) | Q(parent__title__icontains=search))
            if status_param and status_param != 'all':
                if status_param == 'active':
                    query &= Q(publish=True)
                elif status_param == 'inactive':
                    query &= Q(publish=False)
            if icon and icon != 'all':
                query &= Q(icon=icon)

            # Apply filters to database with the constructed query
            menus = menus.filter(query).distinct().order_by('position')

            # Apply sorting
            sort_column= request.GET.get("sort_column", None)
            sort_order= request.GET.get("sort_order", "asc")
            if sort_column:
                if sort_order=="asc":
                    menus = menus.order_by(sort_column)
                else:
                    menus = menus.order_by(f"-{sort_column}")

            # So this line controls how many records per page.
            # /api/menus/?per_page=10   → per_page = 10
            # /api/menus/              → per_page = 50
            per_page = int(request.GET.get("per_page", 10))
            # So this line splits your queryset into pages.
            pagination_data = get_paginated_queryset(menus, request, per_page=per_page)
            # This converts Django model objects → JSON data.
            serializer = MenuSerializer(pagination_data['page_obj'], many=True)

            return Response(
                {
                    "menus": serializer.data,
                    'pagination': {
                        'total': pagination_data['total_items'],
                        'total_pages': pagination_data['total_pages'],
                        'current_page': pagination_data['current_page'],
                        'per_page': pagination_data['per_page'],
                        'page_range': pagination_data['page_range'],
                    },
                    "total": menus.count()
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            raise APIException(f"Error fetching menus: {str(e)}")

    def post(self, request, *args, **kwargs):
        serializer = MenuSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Menu Created Successfully!", "menu": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ParentMenuListView(APIView):
    @permission_required('menus', 'Browse')
    def get(self, request):
        parent_menus = Menu.objects.all()  
        serializer = ParentMenuSerializer(parent_menus, many=True)
        return Response(serializer.data)

class MenuDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            return Response({"message": "Menu Updated Successfully!", "menu": response.data}, status=status.HTTP_200_OK)
        return response

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        if response.status_code == status.HTTP_204_NO_CONTENT:
            return Response({"message": "Menu Deleted Successfully!"}, status=status.HTTP_200_OK)
        return response
