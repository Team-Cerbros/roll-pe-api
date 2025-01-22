from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions

from django.core.mail import send_mail

from django.conf import settings

from utils.response import Response
from utils.functions import generate_email_verification_token, verify_email_token

from user.serializers import UserSerializer, CustomTokenObtainPairSerializer
from user.models import User

from paper.models import Paper

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
@permission_classes([IsAuthenticated])
def logout_api(request):
    refresh_token = request.data.get("refresh")

    if not refresh_token:
        return Response(msg="Refresh token이 없습니다.", status=400)

    try:
        token = RefreshToken(refresh_token)
        token.blacklist()  
    except TokenError as e:
        return Response(msg="유효한 Refresh Token이 아닙니다. ", status=400)

    return Response(msg="로그아웃 되었습니다.", status=200)


### 회원가입 이메일 인증용 API
@api_view(['POST'])
@permission_classes([AllowAny])
def signup_api(request):
    # 회원가입 데이터 처리
    email = request.data.get("email")

    if User.objects.filter(email=email).exists():
        return Response(msg="이미 가입된 이메일입니다.", status=400)

    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        try:
            user = serializer.create(serializer.validated_data)
            # serializer = UserSerializer(user)

        except Exception as e:
            
            return Response(data=serializer.errors, status=400)
        
        # 이메일 인증 토큰 생성
        token = generate_email_verification_token(user)
        activation_url = f"{request.scheme}://{request.get_host()}/api/user/verify-email?token={token}"

        # 이메일 발송
        send_mail(
            subject="이메일 인증을 완료해주세요.",
            message=f"다음 링크를 클릭하여 이메일 인증을 완료하세요: {activation_url}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
        )

        return Response(msg="회원가입이 완료되었습니다. 이메일을 확인해주세요.", status=201)
    else:
        return Response(data=serializer.errors, status=400)


class VerifyEmailAPI(APIView):
    def get(self, request):
        token = request.GET.get("token")
        if not token:
            return Response(msg="토큰이 필요합니다.", status=400)

        try:
            payload = verify_email_token(token)
            user_email = payload["email"]

            # 이메일 인증 완료 처리
            user = User.objects.get(email=user_email)
            user.is_active = True
            user.save()

            return Response(msg="이메일 인증이 완료되었습니다.", status=200)
        except ValueError as e:
            return Response(msg=str(e), status=400)

class ForgotPasswordAPI(APIView):
    
    def get_permissions(self):

        if self.request.method == 'GET':
            return [AllowAny()]  # GET 요청은 모든 사용자 허용
        
        elif self.request.method == 'POST':
            return [IsAuthenticated()]  # POST 요청은 인증된 사용자만 허용
        
        elif self.request.method == 'PATCH':
            return [IsAuthenticated()]  # PATCH 요청은 인증된 사용자만 허용
        
        return super().get_permissions()
    
    def patch(self, request):

        refresh_token = request.data["refresh"]

        password = request.data['newPassword']
        password_check = request.data['newPasswordCheck']
        
        if password != password_check:
            return Response(msg="두 비밀번호가 일치하지 않습니다.", status=400)
        
        user = User.objects.get(email=request.user.email)
        
        user.set_password(password)
        user.save()

        # 리프레시 토큰 무효화 처리 (로그아웃)
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()  
            except Exception as e:
                return Response(msg="토큰 무효화 중 오류가 발생했습니다.", status=400)

        return Response(msg="비밀번호 변경이 완료되었습니다. 다시 로그인해주세요.", status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def myid_in_invate_rollpe_api(request):
    user = request.user

    # invitingUser에 현재 사용자(user)가 포함된 Papers 조회
    papers = Paper.objects.filter(invitingUser=user).distinct()
    
    data = {
        "count": papers.count(),
        "papers": [
            {
                "id": paper.id,
                "title": paper.title,
                "description": paper.description,
                "receivingDate": paper.receivingDate,
            }
            for paper in papers
        ]
    }
    
    return Response(data=data, status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def receiver_is_me_api(request):
    user = request.user
        
    # receiverFK_id가 현재 사용자(user)의 ID인 Papers 조회
    papers = Paper.objects.filter(receiverFK=user).distinct()
    
    data = {
        "count": papers.count(),
        "papers": [
            {
                "id": paper.id,
                "title": paper.title,
                "description": paper.description,
                "receivingDate": paper.receivingDate,
            }
            for paper in papers
        ]
    }
    
    return Response(data=data, status=200)
