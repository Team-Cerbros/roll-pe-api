from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse


class LoginAPITestCase(APITestCase):
    def setUp(self):
        self.UserModel = get_user_model()
        self.login_url = reverse('token_obtain_pair') # 로그인 엔드포인트 URL
        self.signup_url = reverse('signup') # 로그인 엔드포인트 URL
        self.signup_data = {
            "name": "testuser",
            "email": "test@test.com",
            "password": "testpassword",
            "sex": 1,
            "birth": "000101",
            "phoneNumber": "01012345678",
            "is_test":True
        }
        self.client.post(self.signup_url, self.signup_data, format='json')

        self.login_data = {
            'email': 'test@test.com',
            'password': 'testpassword',
        }

    ''' 로그인 성공 '''
    def test_signin_success(self):
        response = self.client.post(self.login_url, self.login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data.get('data'))
        self.assertIn('refresh', response.data.get('data'))

    ''' 로그인 실패 잘못된 데이터 사용 '''
    def test_signin_fail_invalid_data(self):
        data = {
            'email': 'test1111@test.com',
            "password": "wrongpassword"
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('access', response.data)
        self.assertNotIn('refresh', response.data)

    ''' 빈 데이터 '''
    def test_login_fail_empty_fields(self):
        data = {
            "username": "",
            "password": ""
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

