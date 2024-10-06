# chat/middleware.py

from channels.middleware import BaseMiddleware
from django.contrib.auth import get_user_model
from users.models import CustomUser
from django.db import close_old_connections
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser


from django.utils import timezone
import jwt
from django.conf import settings
import datetime
from django.utils.deprecation import MiddlewareMixin

User = get_user_model()

class TokenAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        close_old_connections()
        query_string = scope['query_string'].decode()
        token = None
        if 'token=' in query_string:
            token = query_string.split('token=')[1]
        
        if token:
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                user = await database_sync_to_async(CustomUser.objects.get)(id=payload['user_id'])
                scope['user'] = user
            except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, CustomUser.DoesNotExist):
                scope['user'] = AnonymousUser()
        else:
            scope['user'] = AnonymousUser()
        
        return await super().__call__(scope, receive, send)
    
class UpdateLastSeenMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            CustomUser.objects.filter(id=request.user.id).update(last_seen=timezone.now())

