from rest_framework import status

from utils.response import Response
from rest_framework.views import APIView


class PaperAPI(APIView):
	def get(self, request):
		return Response(
			data="data",
			status=status.HTTP_401_UNAUTHORIZED
			)

