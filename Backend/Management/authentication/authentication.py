from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from services.keycloak_service import KeycloakService
from traceback import print_exc
from accounts.models import Admin

class KeycloakAuthentication(BaseAuthentication):

    def authenticate(self, request):

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return None

        if not auth_header.startswith("Bearer "):
            raise AuthenticationFailed("Invalid Authorization header")

        token = auth_header.split(" ")[1]

        try:
           
            payload = KeycloakService.verify_token(token)

            user, created = Admin.objects.get_or_create(
                keycloak_id=payload["sub"],
                defaults={
                    "username": payload["preferred_username"],
                },
            )
            
            changed = False
            
            username = payload["preferred_username"]
            if user.username != username:
                user.username = username
                changed = True
            
            email = payload.get("email", "")
            if user.email != email:
                user.email = email
                changed = True
            
            full_name = payload.get("name", "")
            if user.full_name != full_name:
                user.full_name = full_name
                changed = True

            roles = payload.get("realm_access", {}).get("roles", [])

            if user.roles != roles:
                user.roles = roles
                changed = True
            
            if changed:
                user.save()
            
            return (user, None)
            
        except Exception as e:
            print("========== JWT ERROR ==========")
            print(type(e).__name__)
            print(e)
            print_exc()
            raise AuthenticationFailed(str(e))