from django.shortcuts import redirect
from django.http import HttpResponseForbidden
from functools import wraps
from utils.permissions import has_permission
from django.http import JsonResponse

def permission_required(menu_slug, permission_type):

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(view, *args, **kwargs):
            request = view.request
            if request.user.is_superuser:
                return view_func(view, *args, **kwargs)
            
            if has_permission(request.user, menu_slug, permission_type):
                return view_func(view, *args, **kwargs)
            else:
                return JsonResponse(
                    {"message": "You do not have permission to access this resource."},
                    status=403,
                )
        
        return _wrapped_view

    return decorator