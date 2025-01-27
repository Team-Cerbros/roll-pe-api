
from django.contrib import admin
from django.urls import path

from paper.apis import UserPaperAPI, PaperAPI, PaperEnterManageAPI

urlpatterns = [
	path('', PaperAPI.as_view(), name='paper_api'),
	path('/user', UserPaperAPI.as_view(), name='paper_api_for_user'),
	path('/enter', PaperEnterManageAPI.as_view(), name='paper_invite_api'),
]
