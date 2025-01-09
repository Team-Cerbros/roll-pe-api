
from django.contrib import admin
from django.urls import path

from paper.apis import UserPaperAPI

urlpatterns = [
	path('', UserPaperAPI.as_view(), name='paper_api_for_user'),
]
