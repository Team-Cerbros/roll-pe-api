from django.urls import path
from .apis import signup_api

urlpatterns = [
    path('signup', signup_api, name='signup'),
]