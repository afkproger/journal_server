from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.utils.deprecation import MiddlewareMixin

class JWTCookieMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path.startswith('/media'):
            return None
        if request.path.startswith('/ws/'):
             return None
        open_paths = ['/api/v1/register/', '/api/v1/auth/', '/api/token/', '/api/v1/chat/']
        if any(request.path.startswith(path) for path in open_paths):
            return None
        if request.method == 'OPTIONS':
            return None
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        
        if not auth_header:
            raise AuthenticationFailed('Authorization header missing')
        if not auth_header.startswith('Bearer '):
            raise AuthenticationFailed('Invalid token format. Use "Bearer <token>"')

