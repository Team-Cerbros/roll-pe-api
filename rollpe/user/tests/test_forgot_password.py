from rest_framework.test import APITestCase
from django.urls import reverse
from user.models import User
from rest_framework import status

class ForgotPasswordTestCase(APITestCase):
    def setUp(self):
        self.signup_url = reverse("signup")
        self.login_url = reverse("token_obtain_pair")
        self.logout_url = reverse("logout")
        self.change_password_url = reverse("forgot_password")

        # 회원가입
        self.sign_up_data = {
            "name": "testuser",
            "email": "test@test.com",
            "password": "testpassword",
            "sex": 1,
            "birth": "000101",
            "phoneNumber": "01012345678",
            "is_test":True
        }
        self.test = self.client.post(self.signup_url, self.sign_up_data, format='json')
        
        # 로그인
        self.sign_in_data = {
            "email": "test@test.com",
            "password": "testpassword"
        }
        self.login_response = self.client.post(self.login_url, self.sign_in_data)
        # 헤더에 토큰 추가
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.login_response.data.get('data').get('access')}')

        self.change_data = {
            'refresh':self.login_response.data.get('data').get('refresh'),
            'newPassword':'testnewpassword',
            'newPasswordCheck':'testnewpassword'
        }

    def test_change_password_success(self):
        """
        비밀번호 변경 후 변경된 비밀번호로 재로그인 성공 테스트
        """
        response = self.client.patch(self.change_password_url, self.change_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('data').get('message'), "비밀번호 변경이 완료되었습니다. 다시 로그인해주세요.")

        # 변경된 비밀번호로 로그인 시도
        new_login_response = self.client.post(self.login_url, {'email':self.sign_in_data.get('email'), 'password':self.change_data.get('newPassword')})
        self.assertEqual(new_login_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', new_login_response.data.get('data'))
        self.assertIn('refresh', new_login_response.data.get('data'))

