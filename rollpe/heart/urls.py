
from django.urls import path
from heart.apis import HeartAPI

urlpatterns = [
    path('', HeartAPI.as_view(), name='heart_api')
]