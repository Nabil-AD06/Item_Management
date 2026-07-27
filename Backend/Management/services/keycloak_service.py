import requests
import jwt
from jwt import PyJWKClient
from django.conf import settings

class KeycloakService:
    @staticmethod
    def get_openid_configuration():
        url =(
            f"{settings.KEYCLOAK_SERVER_URL}"
            f"/realms/{settings.KEYCLOAK_REALM}"
            f"/.well-known/openid-configuration"
        )
        response = requests.get(url)

        response.raise_for_status()

        return response.json()

    @staticmethod
    def get_jwks():
        config = KeycloakService.get_openid_configuration()
        response = requests.get(config["jwks_uri"])
        response.raise_for_status()

        return response.json()

    @staticmethod
    def verify_token(token):
        config=KeycloakService.get_openid_configuration()
        jwks_client = PyJWKClient(config["jwks_uri"])
        signing_key = jwks_client.get_signing_key_from_jwt(token)

        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            audience = settings.KEYCLOAK_CLIENT_ID,
            issuer=settings.KEYCLOAK_ISSUER,
        )

        return payload

    @staticmethod
    def get_admin_token():
        url =(
            f"{settings.KEYCLOAK_SERVER_URL}"
            f"/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/token"
        )

        data = {
            "grant_type": "client_credentials",
            "client_id": settings.KEYCLOAK_CLIENT_ID,
            "client_secret": settings.KEYCLOAK_CLIENT_SECRET,
        }

        response = requests.post(url, data=data)
        response.raise_for_status()

        return response.json()["access_token"]

    @staticmethod
    def update_user(keycloak_id, username, email):
        admin_token = KeycloakService.get_admin_token()
        url = (

            f"{settings.KEYCLOAK_SERVER_URL}"
            f"/admin/realms/{settings.KEYCLOAK_REALM}"
            f"/users/{keycloak_id}"
            )
        headers = {
            "Authorization": f"Bearer {admin_token}",
            "Content-Type": "application/json",
            }
        data = {
            "username": username,
            "email": email,
            "enabled": True
        }
        response = requests.put(
            url,
            headers=headers,
            json=data,
        )
        response.raise_for_status()