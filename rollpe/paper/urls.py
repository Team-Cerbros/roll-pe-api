
from django.contrib import admin
from django.urls import path

from paper.apis import PaperAPI

urlpatterns = [
	path('test', PaperAPI.as_view(), name='test'),
]
