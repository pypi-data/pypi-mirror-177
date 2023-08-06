""" Hosts Middlewares for Teacher Training. """
import logging

import requests
from django.conf import settings
from django.http import JsonResponse

log = logging.getLogger("gunicorn.error")

class AuthenticationMiddleware:
    """Middleware for request token validation."""

    def __init__(self, get_response):
        """Set the get response to get response of view."""
        self.get_response = get_response

    def is_valid_token(self, token):
        """
        Send request to auth service and validate token.
        """
        resp = requests.post(
            settings.KONG_BASE_URL + "/tokens/verify/",
            data={"token": token},
            verify=False,
        )
        try:
            data_json = resp.json()
        except Exception as e:
            return False, {"detail": "Token is invalid or expired"}, 401

        if resp.status_code == 401:
            return False, data_json, resp.status_code
        if resp.status_code == 200:
            return True, data_json, resp.status_code
        
        return False, {"detail": "Token is invalid or expired"}, 401

    def __call__(self, request):
        """Validate access token before processing the endpoint."""
        try:
            # Get the token from request
            token = request.META.get("HTTP_AUTHORIZATION")
            # Exclude this middleware for admin site
            if request.path.startswith("/management"):
                return self.get_response(request)
            if not token:
                return JsonResponse(
                    {"Error": "Authentication Token is Missing"}, safe=False, status=401
                )
            else:
                token = token.split(" ")[1]

            # Validate Token
            is_valid, json_data, status_code = self.is_valid_token(token)

            # Same Response in case of invalid token
            if not is_valid:
                return JsonResponse(json_data, safe=False, status=status_code)

            # Add user data to request Json
            request.user_data = json_data["data"]

            # Call the view for new request and continue.
            response = self.get_response(request)

            return response
        except Exception as e:
            log.exception(
                f"Exception Occured during token authentication"
                f"Exception: {e}"
            )
            return JsonResponse({"detail": "Token is invalid or expired"}, 401)