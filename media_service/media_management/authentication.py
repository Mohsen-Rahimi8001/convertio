import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from django.contrib.auth.models import AnonymousUser

class AuthenticatedUser(AnonymousUser):
    
    def __init__(self, payload):
        super().__init__()
        self.payload = payload
        
    @property
    def is_authenticated(self):
        return True


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        
        access = request.headers.get("Authorization")
        
        if not access or not access.startswith("Bearer "):
            return None
        
        access = access.split()[1]
        
        try:
            payload = jwt.decode(access, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token expired")
        
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token")

        return AuthenticatedUser(payload), None