from rest_framework.response import Response
from rest_framework.views import APIView
from administrator.roles.models import Roles
from django.contrib.auth.models import User
from administrator.menus.models import Menu
from administrator.permission_type.models import PermissionType
class DropdownView(APIView):
    def get(self, request):
        datas = {}

        #! Role Name
        if request.GET.get("role_names"):
            search_term = request.GET.get("query", "")
            datas["role_name"] = self.getRoleName(search_term)
        
        #! Username
        if request.GET.get("usernames"):
            search_term = request.GET.get("query", "")
            datas["username"] = self.getUserName(search_term)

        #! Menu
        if request.GET.get("titles"):
            search_term = request.GET.get("query", "")
            datas["title"] = self.getTitle(search_term)

        if request.GET.get('permission_types'):
            search_term = request.GET.get("query", "")
            datas["permission_type"] = self.getName(search_term)
        return Response(datas)

    # ! Role Name   
    def getRoleName(self, search_term=""):
        if search_term and len(search_term) >= 2:
            role_names = Roles.objects.filter(role_name__icontains=search_term)
            return list(role_names.values("id", "role_name"))
        else:
            role_names = Roles.objects.all()
            return list(role_names.values())

    # ! Username
    def getUserName(self, search_term=""):
        if search_term and len(search_term) >= 2:
            usernames = User.objects.filter(username__icontains=search_term)
            return list(usernames.values("id", "username"))
        else:
            usernames = User.objects.all()
            return list(usernames.values())
    
    # ! Menu Title
    def getTitle(self, search_term=""):
        if search_term and len(search_term) >= 2:
            titles = Menu.objects.filter(title__icontains=search_term)
            return list(titles.values("id", "title"))
        else:
            titles = Menu.objects.all()
            return list(titles.values())
    
    # ! Permission Type
    def getName(self, search_term=""):
        if search_term and len(search_term) >= 2:
            permission_types = PermissionType.objects.filter(name__icontains=search_term)
            return list(permission_types.values("id", "name"))
        else:
            permission_types = PermissionType.objects.all()
            return list(permission_types.values())