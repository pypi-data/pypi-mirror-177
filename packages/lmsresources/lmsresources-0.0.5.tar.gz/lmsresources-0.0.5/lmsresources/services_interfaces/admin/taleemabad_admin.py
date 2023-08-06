import requests
from django.conf import settings

def signup_request(data):
    return requests.post(
            url=settings.KONG_BASE_URL + "/signup/",
            data=data,
            verify=False,
        )

def deactivate_user_request(user_uuid):
    return requests.post(
            url=settings.KONG_BASE_URL + "/deactivate_user",
            params={"uuid": user_uuid},
            verify=False,
        )

def update_user_request(user_uuid, role):
    return requests.patch(
            url=f"{settings.KONG_BASE_URL}/update_user/{user_uuid}",
            json={"role": role},
            verify=False)