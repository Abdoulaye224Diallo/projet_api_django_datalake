import json
from datetime import datetime
from django.utils.deprecation import MiddlewareMixin
from .models import AccessLog
from django.contrib.auth.models import AnonymousUser

class APILoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Ignore admin
        if request.path.startswith('/admin'):
            return

        user = request.user if request.user and not isinstance(request.user, AnonymousUser) else None
        token = request.META.get('HTTP_AUTHORIZATION', '').replace('Token ', '') or None
        body = ''
        try:
            if request.body:
                body = request.body.decode('utf-8')
                # Convert bytes to readable JSON string if possible
                try:
                    body = json.dumps(json.loads(body), indent=2)
                except:
                    pass
        except:
            body = '[unable to decode body]'

        AccessLog.objects.create(
            user=user,
            token=token,
            path=request.path,
            method=request.method,
            body=body
        )
