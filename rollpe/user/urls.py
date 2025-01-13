from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from .apis import signup_api, CustomTokenObtainPairAPI

urlpatterns = [
    # path('signin', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('signin', CustomTokenObtainPairAPI.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup', signup_api, name='signup'),
]