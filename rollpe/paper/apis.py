from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination

from paper.serializer import UserShowPaperSerializer, PaperCreateSerializer, PaperSerializer, QueryIndexSerializer, \
	QueryIndexCreateSerializer
from user.models import User
from utils.response import Response
from rest_framework.views import APIView

from utils.share.functions import is_invited_user
from .models import Paper, QueryIndexTable


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


	def delete(self, request):
		user = User.objects.get(pk=request.user.id)
		paper = Paper.objects.get(code=request.data['pcode'])

		if paper.hostFK == user:
			paper.delete()
			return Response(status=status.HTTP_204_NO_CONTENT)
		else:
			if paper.invitingUser.filter(pk=user.pk).exists():
				return Response(status=470)
			else:
				return Response(status=471)



class PaperAPI(APIView):
	def get(self, request):
		pcode = request.query_params.get('pcode', None)

		if pcode is None:
			return Response(
				msg="pcode가 필요합니다.",
				status=status.HTTP_404_NOT_FOUND
				)

		if not request.user.is_authenticated:
			return Response(status=401)

		user = User.objects.get(pk=request.user.id)
		try:

			paper = Paper.objects.get(code=pcode)
		except Paper.DoesNotExist as e:
			return Response(msg=str(e), status=status.HTTP_404_NOT_FOUND)

		response = PaperSerializer(paper).data

		if is_invited_user(user, paper):
			return Response(
				data=response,
				status=status.HTTP_200_OK
				)
		else:
			return Response(status=471)

	def post(self, request):
		serializer = PaperCreateSerializer(data=request.data)
		if serializer.is_valid():
			paper = serializer.save()
			return Response(
				data=PaperCreateSerializer(paper).data,
				status=status.HTTP_201_CREATED
				)
		return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QueryIndexAPI(APIView):
	def get(self, request):
		query_type = request.data.get("type", "all").upper()

		if query_type == "ALL":
			queryset = QueryIndexTable.objects.all()
		else:
			queryset = QueryIndexTable.objects.filter(type=query_type)

		response = QueryIndexSerializer(queryset, many=True).data

		return Response(
			data=response,
			status=status.HTTP_200_OK
		)

	def post(self, request):
		serializer = QueryIndexCreateSerializer(data=request.data)
		if serializer.is_valid():
			index = serializer.save()
			return Response(
				data=QueryIndexSerializer(index).data,
				status=status.HTTP_201_CREATED
				)
		return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaperEnterManageAPI(APIView):
	def post(self, request):
		pcode = request.data.get('pcode', None)

		if pcode is None:
			return Response(
				msg="pcode가 없습니다.",
				status=status.HTTP_400_BAD_REQUEST
				)

		if not request.user.is_authenticated:
			return Response(status=401)

		user = User.objects.get(pk=request.user.id)

		try:
			paper = Paper.objects.get(code=pcode)
		except Paper.DoesNotExist as e:
			return Response(msg=str(e), status=status.HTTP_404_NOT_FOUND)

		request_password = request.data.get('password', None)



		if paper.invitingUser.filter(pk=user.pk).exists():
			return Response(status=473)

		if paper.viewStat:
			paper.invitingUser.add(user)
			return Response(
				msg="추가 되었습니다.",
				status=status.HTTP_204_NO_CONTENT
				)
		else:
			if request_password is None:
				return Response(
					msg="password가 없습니다.",
					status=status.HTTP_400_BAD_REQUEST
					)

			if check_password(request_password, paper.password):
				paper.invitingUser.add(user)
				return Response(
					msg="추가 되었습니다.",
					status=status.HTTP_204_NO_CONTENT
					)
			else:
				return Response(status=472)