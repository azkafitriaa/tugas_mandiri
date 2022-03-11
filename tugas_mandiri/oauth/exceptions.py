from rest_framework.exceptions import APIException


class InvalidRequest(APIException):
    status_code = 401
    default_detail = {"error": "invalid_request", "error_description": "Invalid request"}

class AuthenticationFailed(APIException):
    status_code = 401
    default_detail = {"error": "auth_failed", "error_description": "Authentication failed"}

class AuthorizationFailed(APIException):
    status_code = 401
    default_detail = {"error": "not_authorized", "error_description": "Not Authorized"}

class ExpiredToken(APIException):
    status_code = 401
    default_detail = {"error": "expired_token", "error_description": "Expired token"}

class InvalidToken(APIException):
    status_code = 401
    default_detail = {"error": "invalid_token", "error_description": "Invalid token"}