from django.http import JsonResponse
from rest_framework import status

from utils.constants import SystemCodeManager


class CustomResponse(JsonResponse):
	def __init__(self, data=None, **kwargs):
		http_status = kwargs.pop("status", status.HTTP_200_OK)

		code = SystemCodeManager.get_code(http_status)
		msg = kwargs.pop("msg", SystemCodeManager.get_message(http_status))
		link = kwargs.pop("link", SystemCodeManager.get_link(http_status))

		# 최종 payload의 형태를 원하는 대로 구성
		payload = {
			"status_code": http_status,
			"message": msg,
			"code": code,
			"link": link,
			"data": data,
			}

		super().__init__(payload, status=http_status, **kwargs)

	def set_cookie(self, key, value, **options):
		"""
		Wrapper for setting a cookie on the response.
		"""
		self.cookies[key] = value
		for option_key, option_value in options.items():
			setattr(self.cookies[key], option_key, option_value)


def Response(**kwargs):
	return CustomResponse(**kwargs)
