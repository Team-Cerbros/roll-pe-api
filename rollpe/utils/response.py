from rest_framework.response import Response
from rest_framework import status

# 예시: SystemCodeManager는 프로젝트 특성에 맞춰 자유롭게 작성/수정
from utils.constants import SystemCodeManager


class CustomResponse(Response):
	def __init__(self, data=None, **kwargs):
		http_status = kwargs.pop("status", status.HTTP_200_OK)

		code = SystemCodeManager.get_code(http_status)
		msg = SystemCodeManager.get_message(http_status)
		link = kwargs.pop("link", SystemCodeManager.get_link(http_status))

		# 최종 payload의 형태를 원하는 대로 구성
		payload = {
			"status_code": http_status,
			"message": msg,
			"code": code,
			"link": link,
			"data": data,
			}

		# Response의 초기화는 최종 payload와 kwargs를 넘겨줍니다.
		super().__init__(payload, status=http_status, **kwargs)

def Response(**kwargs):
	"""
	DRF의 Response가 아닌 custom Response를 간단하게 호출하기 위한 함수.
	return Response(data=...) 형태로 사용할 수 있도록 만든다.
	"""
	return CustomResponse(**kwargs)
