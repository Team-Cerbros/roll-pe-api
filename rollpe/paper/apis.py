from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination

from paper.serializer import UserShowPaperSerializer, PaperCreateSerializer
from user.models import User
from utils.response import Response
from rest_framework.views import APIView

from .models import Paper


class UserPaperAPI(APIView):
	pagination_class = PageNumberPagination

	def get(self, request):
		queryset = Paper.objects.all().order_by('-createdAt')
		paginator = self.pagination_class()
		page = paginator.paginate_queryset(queryset, request)  # <- 페이지 분할

		if queryset.count() == 0:
			return Response(status=status.HTTP_404_NOT_FOUND)

		serializer = UserShowPaperSerializer(page, many=True)

		return Response(
			data=paginator.get_paginated_response(serializer.data).data,
			status=status.HTTP_200_OK
		)


	def post(self, request):
		serializer = PaperCreateSerializer(data=request.data)
		if serializer.is_valid():
			paper = serializer.save()
			return Response(
				data=PaperCreateSerializer(paper).data,
				status=status.HTTP_201_CREATED
				)
		return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def delete_paper(request):
	user = User.objects.get(id=request.user.id)
