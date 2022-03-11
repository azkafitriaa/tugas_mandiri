from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter
from .views import SessionViewSet, TokenViewSet, ProfileViewSet

# router = DefaultRouter()
# router.register(r'token', SessionViewSet)
router = SimpleRouter(trailing_slash=False)
router.register("token", SessionViewSet, basename="session")
router.register("verify-token", TokenViewSet, basename="verify_token")
router.register("resource", ProfileViewSet, basename="profile")


# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]

