from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse


# Create your tests here.
class SignupTestCase(APITestCase):

    def setUp(self):
        self.signup_url = reverse('signup')
        self.data = {
            'name': 'testuser',
            'email': 'test@test.com',
            'password': 'testpassword',
        }

    """회원가입 성공 Test"""
    def test_signup_success(self):
        response = self.client.post(self.signup_url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)