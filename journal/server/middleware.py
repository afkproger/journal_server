from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.utils.deprecation import MiddlewareMixin

class JWTCookieMiddleware(MiddlewareMixin):
    def process_request(self, request):
        access_token = request.COOKIES.get('access')

        if request.path.startswith('/api/v1/register') or request.path.startswith('/api/v1/auth'):
            return None
        
        if access_token:
            request.META['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'

        if not access_token:
            raise AuthenticationFailed('Authorization token missing')

