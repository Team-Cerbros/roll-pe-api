from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from utils.response import Response
from rest_framework import status
from .serializers import UserSerializer, CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairAPI(TokenObtainPairView):

    def post(self, request, *args, **kwargs):

        serializer = CustomTokenObtainPairSerializer(data=request.data)

        if serializer.is_valid():

            response_data = serializer.validated_data
            
            return response_data  # Response 내부에서 반환된 값을 그대로 전달
        else:
            # 실패 시 errors 반환
            return Response(data=serializer.errors, status=400)

@api_view(['POST'])
@permission_classes([AllowAny])
def signup_api(request):

    serializer = UserSerializer(data=request.data)
    
    if serializer.is_valid():
        try:

            user = serializer.create(serializer.validated_data)
            serializer = UserSerializer(user)

        except Exception as e:
            
            return Response(data=serializer.errors, status=400)
        
        return Response(status=201)
    else:
        return Response(data=serializer.errors, status=400)