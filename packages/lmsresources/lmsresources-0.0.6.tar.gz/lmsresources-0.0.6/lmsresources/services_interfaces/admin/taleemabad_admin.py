import requests
from django.conf import settings


def signup_request(data):
    return requests.post(
            url=settings.KONG_BASE_URL + "/auth/signup/",
            data=data,
            verify=False,
        )


def deactivate_user_request(user_uuid):
    return requests.post(
            url=settings.KONG_BASE_URL + "/auth/deactivate_user",
            params={"uuid": user_uuid},
            verify=False,
        )


def update_user_request(user_uuid, role):
    return requests.patch(
            url=f"{settings.KONG_BASE_URL}/auth/update_user/{user_uuid}",
            json={"role": role},
            verify=False)


def get_user_data(uuid):
    """
    Get user info
    """
    return requests.get(
        url=settings.KONG_BASE_URL + "/auth/list_users",
        params={"id": uuid},
        verify=False,
    ).json()


def get_school(school_uuid, token):
    """
    Get School details for UUID.
    """
    return requests.get(
        url=settings.KONG_BASE_URL + f"/school/schools/{school_uuid}",
        headers={"Authorization": token},
        verify=False,
    ).json()


def get_school_teachers_role_based(school_uuid):
    """
    Get all school teachers.
    """
    return requests.get(
        url=settings.KONG_BASE_URL + "/auth/list_users",
        params={"school": school_uuid, "role": "TEACHER"},
        verify=False,
    ).json()


def get_school_admins(school_uuid):
    """
    Get all school admins.
    """
    return requests.get(
        url=settings.KONG_BASE_URL + "/auth/list_users",
        params={"school": school_uuid, "roles": "ADMIN,SUPERUSER"},
        verify=False,
    ).json()


def get_school_teacher_info(uuid):
    """
    Get school teacher.
    """
    return requests.get(
        url=settings.KONG_BASE_URL + "/auth/list_users",
        params={"id": uuid, "role": "TEACHER"},
        verify=False,
    ).json()


def get_lesson_plan_status(token, start_date, end_date):
    """
    Get all school teachers.
    """
    return requests.get(
        url=settings.KONG_BASE_URL + "/content/apis/teacher-lesson-plan-status",
        params={"date_time_start": start_date, "date_time_end": end_date},
        headers={"Authorization": token},
        verify=False,
    ).json()


def get_teacher_training_status(token, start_date, end_date):
    return requests.get(
        url=settings.KONG_BASE_URL + "/teacher-training/apis/teachertrainingstatus",
        params={"date_time_start": start_date, "date_time_end": end_date},
        headers={"Authorization": token},
        verify=False,
    ).json()
