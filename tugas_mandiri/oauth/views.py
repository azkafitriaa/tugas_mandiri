from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import random, string, requests
from .serializers import CreateSessionRequest, CreateSessionResponse, VerifyTokenResponse, GetProfileResponse
from .models import Client, Profile, Session
from .exceptions import InvalidRequest, AuthenticationFailed, AuthorizationFailed, ExpiredToken, InvalidToken

######################### ganti ###############################
URL = 'http://localhost:8000/'

class SessionViewSet(viewsets.ViewSet):
    def create(self, request: Request) -> Response:
        """
        Create a new session and generate token
        """
        if request.content_type == 'application/x-www-form-urlencoded':
            try:
                serializer = CreateSessionRequest(data=request.data)
                serializer.is_valid(raise_exception=True)
                data = serializer.data
                client_id = data["client_id"]
                client_secret = data["client_secret"]
                grant_type = data["grant_type"]
                username = data["username"]
                password = data["password"]

                client = Client.objects.get(id=client_id, secret=client_secret)
                user = authenticate(username=username, password=password)
                
                if user and grant_type == 'password':
                    access_token = ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=40))
                    refresh_token = ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=40))
                    expires_in = timezone.now() + timedelta(minutes=5)

                    new_session = Session(
                        client=client,
                        user=user,
                        access_token = access_token,
                        expires_in = expires_in,
                        refresh_token = refresh_token
                    )
                    new_session.save()
                    return Response(CreateSessionResponse({
                        "access_token": access_token,
                        "expires_in": 300,
                        "token_type": "Bearer",
                        "scope": "null",
                        "refresh_token": refresh_token
                    }).data)
                raise AuthenticationFailed()
            except Client.DoesNotExist:
                raise AuthenticationFailed() 
            except AuthenticationFailed:
                raise AuthenticationFailed()
            except:
                raise InvalidRequest()
        raise InvalidRequest() 
                       

class TokenViewSet(viewsets.ViewSet):
    def create(self, request: Request) -> Response:
        """
        Verify token
        """
        try:
            authorization = request.headers['Authorization']
            authorization = authorization.split()
            token = authorization[1]
            session = Session.objects.get(access_token=token)
            
            is_expired = session.expires_in.replace(tzinfo=timezone.utc).astimezone(tz=None) <= timezone.now()
            
            if is_expired:
                raise ExpiredToken()
            return Response(VerifyTokenResponse({
                "client_id": session.client.id,
                "user_id": session.user.id,
                "access_token": session.access_token,
                "expires_in": "null",
                "token_type": "Bearer",
                "scope": "null",
                "refresh_token": session.refresh_token
            }).data)
        except Session.DoesNotExist:
            raise InvalidToken()
        except ExpiredToken:
            raise ExpiredToken()
        except:
            raise InvalidRequest()

class ProfileViewSet(viewsets.ViewSet):
    def create(self, request: Request) -> Response:
        """
        Get user profile
        """
        try:
            authorization = request.headers['Authorization']
            authorization = authorization.split()
            token = authorization[1]
            headers = {'Authorization': 'Bearer ' + token}
            validate_token = requests.post(URL + 'oauth/verify-token', headers=headers)

            if validate_token.status_code == 200:
                data = validate_token.json()
                access_token = data["access_token"]
                refresh_token = data["refresh_token"]
                client_id = data["client_id"]

                user_id = data["user_id"]
                user = User.objects.get(id=user_id)

                profile = Profile.objects.get(user=user)
                npm = profile.npm
                full_name = profile.full_name

                return Response(GetProfileResponse({
                    "access_token": access_token,
                    "client_id": client_id,
                    "user_id": user_id,
                    "full_name": full_name,
                    "npm": npm,
                    "expires_in": "null",
                    "refresh_token": refresh_token,
                }).data)
            raise AuthorizationFailed()   
        except AuthorizationFailed:
            raise AuthorizationFailed()     
        except:
            raise InvalidRequest() 
