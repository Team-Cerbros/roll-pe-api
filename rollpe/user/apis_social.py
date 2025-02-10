from django.shortcuts import redirect

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken

from utils.env import return_env_value
from utils.response import Response

import requests

@api_view(['GET'])
def social_login(request, provider):

    # code = request.data.get('code')
    code = request.GET.get('code')
    
    match provider:

        case "kakao":
            
            user_instance = kakao_login(request,code)
        
        case "google":

            user_instance = google_login(request,code)
    
    # user_instance로 토큰 발급
    # tokens = get_tokens_for_user(user)

    return Response(status=200)

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def kakao_login(request, code):
    client_id = return_env_value("SOCIAL_AUTH_KAKAO_CLIENT_ID")

    call_back_url = f"http://localhost:8000/api/user/social/login/kakao"

    get_kakao_token = requests.post(
        "https://kauth.kakao.com/oauth/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "grant_type": "authorization_code",
            "client_id": client_id,
            "redirect_uri": call_back_url,
            "code": code
        },
    )
    kakao_token = get_kakao_token.json()

    access_token = kakao_token.get("access_token")

    user_kakao_account = requests.get(
        "https://kapi.kakao.com/v2/user/me",
        headers={"Authorization": f"Bearer {access_token}"},
    ).json()
    print(user_kakao_account)
    # {
    #     'id': 3906883889, 'connected_at': '2025-02-04T10:58:47Z', 
    #     'properties': {
    #         'nickname': '김재희'
    #     }, 
    #     'kakao_account': {
    #         'profile_nickname_needs_agreement': False, 
    #         'profile': {
    #             'nickname': '김재희', 
    #             'is_default_nickname': False
    #         }
    #     }
    # }

    # {
    #     "name": "testuser",
    #     "email": "wogml8524@naver.com",
    #     "password": "testpassword",
    #     "sex": 1,
    #     "birth": "000101",
    #     "phoneNumber": "01012345678"
    # }

    # user_kakao_account에서email 가져오기

    # 가져온 이메일로 사용자 생성 및 조회후 return user_instance 
    # user, created = User.objects.get_or_create(
    #     email=email,
    #     defaults={'username': email.split('@')[0]}
    # )
    
    return 

def google_login(request, code):

    return

class KakaoLoginView(APIView):
    def get(self, request):
        client_id = return_env_value("SOCIAL_AUTH_KAKAO_CLIENT_ID")
        redirect_uri = "http://localhost:8000/api/user/social/login/kakao"
        return redirect(
            f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
        )