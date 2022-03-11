from rest_framework import serializers
from .models import Session

class CreateSessionRequest(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    grant_type =serializers.CharField()
    client_id = serializers.CharField()
    client_secret = serializers.CharField()

class CreateSessionResponse(serializers.Serializer):
    access_token = serializers.CharField()
    expires_in = serializers.IntegerField()
    token_type = serializers.CharField()
    scope = serializers.CharField()
    refresh_token = serializers.CharField()

class VerifyTokenResponse(serializers.Serializer):
    client_id = serializers.CharField()
    user_id = serializers.CharField()
    access_token = serializers.CharField()
    expires_in = serializers.CharField()
    token_type = serializers.CharField()
    scope = serializers.CharField()
    refresh_token = serializers.CharField()

class GetProfileResponse(serializers.Serializer):
    access_token = serializers.CharField()
    client_id = serializers.CharField()
    user_id = serializers.CharField()
    full_name = serializers.CharField()
    npm = serializers.CharField()
    expires_in = serializers.CharField()
    refresh_token = serializers.CharField()