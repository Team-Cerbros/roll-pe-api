from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
import uuid

from utils.response import Response
from paper.models import Paper
from heart.models import Heart
from heart.serializers import HeartSerializer, HeartWriteSerializer


def is_valid_uuid(value):
    try:
        if len(value) == 32:
            value = f"{value[:8]}-{value[8:12]}-{value[12:16]}-{value[16:20]}-{value[20:]}"
        uuid_obj = uuid.UUID(value, version=4)
        return str(uuid_obj) == value
    except (ValueError, TypeError):
        return False


class HeartAPI(APIView):
    """
        * 추가 작업 필요 상황
        비공개면 초대받지 못한 유저의 경우 조회할 수 없도록 제어 필요
    """
    pagination_class = PageNumberPagination
    def get(self, request):
        """
            pcode가 queryparameter에 없거나,
            존재하지 않는 롤링페이퍼일 경우 404 처리
        """
        pcode = request.GET.get('pcode')
        hcode = request.GET.get('hcode')
        
        if hcode:
            # 상세정보 가져오기
            query = Heart.objects.filter(code=hcode)
            if not is_valid_uuid(hcode) or not query.exists():
                return Response(status=404)
            
            queryset = query.get()
            serializer = HeartSerializer(queryset)
            
            return Response(
                data=serializer.data,
                status=200
            )
        else:
            # 목록 가져오기
            if not pcode or not is_valid_uuid(pcode) or not Paper.objects.filter(code=pcode).exists():
                return Response(status=404)
            
            paginator = self.pagination_class()
            queryset = Heart.objects.filter(paperFK__code=pcode).all().order_by('createdAt')
            
            page = paginator.paginate_queryset(queryset, request)
            serializer = HeartSerializer(page, many=True)
            
            return Response(
                data=paginator.get_paginated_response(serializer.data).data,
                status=200
            )
            
    
    def post(self, request):
        """
            * 추가 작업 필요 상황
            이미 작성했으면 못작성하도록 제어 필요
            비공개면 초대받지 못한 유저의 경우 작성할 수 없도록 제어 필요
        """
        serializer = HeartWriteSerializer(data=request.data, method='post')
        if not serializer.is_valid():
            return Response(status=400)
        heart_instance = serializer.create(serializer.validated_data)
        return Response(status=201)
    
    
    def patch(self, request):
        """
            본인이 작성한 게시물이 맞는지, 초대받은 유저가 맞는지 검증 필요
            로그인 구현되면 코드 추가할 것
        """
        serializer = HeartWriteSerializer(data=request.data, method='patch')
        if not serializer.is_valid():
            return Response(status=400)
        heart_instance = serializer.update(serializer.validated_data)
        return Response(status=200)
        