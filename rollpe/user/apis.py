from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def signup_api(request):

    serializer = UserSerializer(data=request.data)
    
    if serializer.is_valid():
        print(serializer.validated_data)
        try:

            user = serializer.create(serializer.validated_data)
            serializer = UserSerializer(user)

        except Exception as e:
            
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        return Response(status=status.HTTP_201_CREATED)
    else:
        print(serializer.errors)
        response_data = {
            'message': serializer.errors
        }
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)