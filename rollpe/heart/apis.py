from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination

from utils.response import Response
from paper.models import Paper
from heart.models import Heart
from heart.serializers import HeartSerializer

""" 
    paper에 uuid 필드 생기면 수정 필요 
"""
class HeartAPI(APIView):
    pagination_class = PageNumberPagination
    
    def get(self, request):
        """
            pid가 queryparameter에 없거나,
            존재하지 않는 롤링페이퍼일 경우 404 처리
        """
        pid = request.GET.get('pid')
        if not pid or not Paper.objects.filter(pk=pid).exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        paginator = self.pagination_class()
        queryset = Heart.objects.filter(paperFK=pid).all().order_by('-createdAt')
        
        page = paginator.paginate_queryset(queryset, request)
        serializer = HeartSerializer(page, many=True)
        
        return Response(
			data=paginator.get_paginated_response(serializer.data).data,
			status=status.HTTP_200_OK
        )
        
        