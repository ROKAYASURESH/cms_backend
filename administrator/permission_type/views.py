from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import UpdateAPIView, DestroyAPIView
from rest_framework.exceptions import APIException
from .models import PermissionType
from .serializers import PermissionTypeSerializer
from utils.paginators import get_paginated_queryset
from decorators.decorators import permission_required

class PermissionTypeAPIView(APIView):
    @permission_required('permission_type', 'Browse')
    def get(self, request, *args, **kwargs):
        try:
            permission_types = PermissionType.objects.all().order_by('id')
            name = request.GET.getlist('name[]', '')
            is_active = request.GET.get('is_active', None)
            created_at = request.GET.get('created_at', '')

            if name:
                permission_types = permission_types.filter(id__in=name)
                
            if is_active is not None:
                is_active = is_active.lower() == 'true'  # Convert to boolean (True/False)

            if is_active is not None:
                permission_types = permission_types.filter(is_active=is_active)
                
            if created_at:
                permission_types = permission_types.filter(created_at__icontains=created_at)

            sort_column = request.GET.get('sort_column', 'id')
            sort_order = request.GET.get('sort_order', 'asc')
            
            if sort_order == 'desc':
                sort_column = f'-{sort_column}'
            permission_types = permission_types.order_by(sort_column)

            per_page = int(request.GET.get('per_page', 10))
            pagination_data = get_paginated_queryset(permission_types, request, per_page=per_page)
            serializer = PermissionTypeSerializer(pagination_data['page_obj'], many=True)

            return Response({
                'permissions': serializer.data,
                'pagination': {
                    'total': pagination_data['total_items'],
                    'total_pages': pagination_data['total_pages'],
                    'current_page': pagination_data['current_page'],
                    'per_page': pagination_data['per_page'],
                    'page_range': pagination_data['page_range'],

                },
            }, status=status.HTTP_200_OK)

        except Exception as e:
            raise APIException(f"Error fetching permission types: {str(e)}")

    def post(self, request, *args, **kwargs):
        serializer = PermissionTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Permission Type Created Successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PermissionTypeUpdateAPIView(UpdateAPIView):
    queryset = PermissionType.objects.all()
    serializer_class = PermissionTypeSerializer

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            return Response({"message": "Permission Type Updated Successfully!"}, status=status.HTTP_200_OK)
        return response


class PermissionTypeDeleteAPIView(DestroyAPIView):
    queryset = PermissionType.objects.all()
    serializer_class = PermissionTypeSerializer

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        if response.status_code == status.HTTP_204_NO_CONTENT:
            return Response({"message": "Permission Type Deleted Successfully!"}, status=status.HTTP_200_OK)
        return response
