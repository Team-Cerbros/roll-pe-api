from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse


# Create your tests here.
class SignupTestCase(APITestCase):

    def setUp(self):
        self.signup_url = reverse('signup')
        self.data = {
            "name": "testuser",
            "email": "test@test.com",
            "password": "testpassword",
            "sex": 1,
            "birth": "000101",
            "phoneNumber": "01012345678"
        }

    """회원가입 성공 Test"""
    def test_signup_success(self):
        response = self.client.post(self.signup_url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    """잘못된 이메일 형식으로 회원가입 시도 test"""
    def test_signup_with_invalid_email(self):
        self.data['email'] = 'invalid-email'
        response = self.client.post(self.signup_url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    """중복된 이메일로 회원가입 test"""
    def test_signup_with_duplicate_email(self):
        self.client.post(self.signup_url,self.data, format='json')
        response = self.client.post(self.signup_url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
