import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail

def generate_email_verification_token(email):
    payload = {
        "email": email,
        "exp": datetime.utcnow() + timedelta(minutes=5),  # 토큰 만료 시간 (5분)
        "iat": datetime.utcnow(),  # 토큰 발행 시간
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

    return token

def verify_email_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

        # 캐시에서 토큰 조회
        used_token = cache.get(f'{payload["email"]}_token', None)

        if used_token:
            raise ValueError("이미 사용된 토큰입니다.")
        
        cache.set(f'{payload["email"]}_token',token, timeout=300)

        return payload  # 유효한 경우 페이로드 반환
    
    except jwt.ExpiredSignatureError:
        raise ValueError("토큰이 만료되었습니다.")
    except jwt.InvalidTokenError:
        raise ValueError("유효하지 않은 토큰입니다.") 

def generate_send_email(request, email, path_code):
    token = generate_email_verification_token(email)
    activation_url = f"{request.scheme}://{request.get_host()}/api/user/verify-email?path_code={path_code}&token={token}"

    # 이메일 발송
    send_mail(
        subject="이메일 인증을 완료해주세요.",
        message=f"다음 링크를 클릭하여 이메일 인증을 완료하세요: {activation_url}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
    )
    return