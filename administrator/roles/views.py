from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView, DestroyAPIView
from .models import Roles
from .serializers import RoleSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException
from utils.paginators import get_paginated_queryset

class RoleAPIView(APIView):
    
    def get(self, request, *args, **kwargs):
        try:
            roles = Roles.objects.all()

            role_name= request.GET.getlist("role_name[]", None)
            descriptions = request.GET.get("descriptions[]", "")
            isRole = request.GET.get("isRole", None)
            if role_name:
                roles = roles.filter(role_name__in=role_name)
            if descriptions:
                roles = roles.filter(descriptions__icontains=descriptions)
            if isRole is not None:
                if isRole.lower() == 'true':
                    roles = roles.filter(isRole=True)
                elif isRole.lower() == 'false':
                    roles = roles.filter(isRole=False)
            sort_Column= request.GET.get("sort_column", None)
            sort_Order= request.GET.get("sort_order", "asc")
            if sort_Column:
                if sort_Order=="asc":
                    roles = roles.order_by(sort_Column)
                else:
                    roles = roles.order_by(f"-{sort_Column}")
            per_page= int(request.GET.get("per_page", 3))
            pagination_data= get_paginated_queryset(roles, request, per_page=per_page)
            serializer = RoleSerializer(pagination_data['page_obj'], many=True)
            return Response(
                {
                    "roles": serializer.data,
                    'pagination': {
                        'total': pagination_data['total_items'],
                        'total_pages': pagination_data['total_pages'],
                        'current_page': pagination_data['current_page'],
                        'per_page': pagination_data['per_page'],
                        'page_range': pagination_data['page_range'],
                    },
                    "total": roles.count()
                
                 
                 }, 
                            status=status.HTTP_200_OK)
        except Exception as e:
            raise APIException(str(e))

    def post(self, request, *args, **kwargs):
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            parents = request.data.get("parents", [])
            role = serializer.save()
            if parents:
                role.parents.set(parents)
            return Response(
                {"message": "Role Created Successfully!", "role": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RolesUpdateAPIView(UpdateAPIView):
    """
    API endpoint for updating a Role
    """
    queryset = Roles.objects.all()
    serializer_class = RoleSerializer

    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if serializer.is_valid():
            parents = request.data.get("parents", None)
            role = serializer.save()
            
            if parents is not None:
                role.parents.set(parents)
                
            return Response(
                {"message": "Role Updated Successfully!", "role": serializer.data},
                status=status.HTTP_200_OK,
            )
                
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RolesDeleteAPIView(DestroyAPIView):
    """
    API endpoint for deleting a Role
    """
    queryset = Roles.objects.all()
    serializer_class = RoleSerializer

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        if response.status_code == status.HTTP_204_NO_CONTENT:
            return Response(
                {"message": "Role Deleted Successfully!"}, status=status.HTTP_200_OK
            )
        return response

