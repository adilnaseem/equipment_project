from django.utils.deprecation import MiddlewareMixin
from .models import ChangeLog

class ChangeLogMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if request.method in ['POST', 'PUT', 'DELETE']:
            user = request.user if request.user.is_authenticated else None
            model_name = request.resolver_match
            object_id =0 #request.resolver_match.kwargs.get('pk', None)
            route =request.resolver_match.route #request.method
            if 'edit' in route:
                action = 'Edit'
            elif 'form' in route:
                action = 'Create'
            elif 'delete' in route:
                action = 'Delete'
            else: 
                action = 'Pass'
            
            changes = request.POST.dict()

            ChangeLog.objects.create(
                user=user,
                model_name=model_name,
                object_id=object_id,
                action=action,
                changes=changes
            )
        return response
