class SystemCodeManager:

	CODE_MESSAGES = {
		200: {
			"code": "SUCCESS",
			"link": None,
			"message": "정상 처리되었습니다."
			},
		400: {
			"code": "CLIENT ERROR",
			"link": None,
			"message": "오류가 발생했습니다."
			},
		401: {
			"code": "UNAUTHORIZED",
			"link": "/login",
			"message": "로그인이 필요합니다."
			},
		
		404: {
			"code": "NOT_FOUND",
			"link": None,
			"message": "요청하신 리소스를 찾을 수 없습니다."
			},
		}

	@classmethod
	def get_message(cls, key: int, default: str = None) -> str:
		item = cls.CODE_MESSAGES.get(key)
		if item is not None:
			return item["message"]
		return default or f"Unknown key: {key}"

	@classmethod
	def get_code(cls, key: int, default: str = None) -> str:
		item = cls.CODE_MESSAGES.get(key)
		if item is not None:
			return item["code"]
		return default or f"UNKNOWN_CODE_{key}"

	@classmethod
	def get_link(cls, key: int, default: str = None) -> str:
		item = cls.CODE_MESSAGES.get(key)
		if item is not None:
			return item["link"]
		return default or f"UNKNOWN_CODE_{key}"
