from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.utils.timezone import localtime
from urllib.parse import urlencode
from pprint import pprint

from user.models import User
from paper.models import Paper
from heart.models import Heart


class HeartAPITest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # 테스트 유저 생성
        cls.receiver = User.objects.create(
            name='receiver',
            email='receiver@gmail.com',
            password='1234'
        )
        cls.host = User.objects.create(
            name='host',
            email='host@gmail.com',
            password='1234'
        )
        cls.user1 = User.objects.create(
            name='test_user1',
            email='testuser1@gmail.com',
            password='1234'
        )
        cls.user2 = User.objects.create(
            name='test_user2',
            email='testuser2@gmail.com',
            password='1234'
        )
        # 테스트 롤링페이퍼 생성
        cls.rolling_paper = Paper.objects.create(
            receiverFK=cls.receiver,
            hostFK=cls.host,
            receivingDate='2025-01-10',
            title='테스트 롤링페이퍼',
            description='테스트 입니다.',
            password='1234'
        )
        # 테스트 마음 생성
        cls.heart1 = Heart.objects.create(
            userFK=cls.user1,
            paperFK=cls.rolling_paper,
            context='테스트1 마음입니다.'
        )
        cls.heart2 = Heart.objects.create(
            userFK=cls.user2,
            paperFK=cls.rolling_paper,
            context='테스트2 마음입니다.'
        )
        
        cls.url = reverse('heart_api')
        
        
    def test_get_heart_list(self):
        """
            작성된 마음 목록을 가져올 수 있어야 한다.
        """
        self.maxDiff = None
        
        # API 요청
        pcode = {'pcode': self.rolling_paper.code}
        url_with_params = f'{self.url}?{urlencode(pcode)}'
        
        response = self.client.get(url_with_params)

        # 예상 데이터
        expected_data = {
            'status_code' : status.HTTP_200_OK,
            'message' : '정상 처리되었습니다.',
            'code' : 'SUCCESS',
            'link' : None,
            'data' : {
                'count': 2,
                'next': None,
                'previous': None,
                'results': [
                    {
                        'id': self.heart1.id,
                        'userName': self.heart1.userFK.name,
                        'rollingPaperName': self.heart1.paperFK.title,
                        'context': self.heart1.context,
                        'danger': 0,
                        'createdAt': localtime(self.heart2.createdAt).strftime('%Y.%m.%d')
                    },
                    {
                        'id': self.heart2.id,
                        'userName': self.heart2.userFK.name,
                        'rollingPaperName': self.heart2.paperFK.title,
                        'context': self.heart2.context,
                        'danger': 0,
                        'createdAt': localtime(self.heart1.createdAt).strftime('%Y.%m.%d')
                    }
                ]
            }
        }

        # 응답 상태 코드 확인
        self.assertEqual(response.status_code, status.HTTP_200_OK, '상태코드가 올바르지 않습니다.')
        
        # 응답 데이터 비교
        self.assertDictEqual(response.json(), expected_data, '응답 형식이 올바르지 않습니다.')
        
        
    def test_get_heart_detail(self):
        """
            마음 상세정보를 가져올 수 있어야 한다.
        """
        hcode = {'hcode': self.heart1.code}
        url_with_params = f'{self.url}?{urlencode(hcode)}'
        
        response = self.client.get(url_with_params)
        
        expected_data = {
            'status_code' : status.HTTP_200_OK,
            'message' : '정상 처리되었습니다.',
            'code' : 'SUCCESS',
            'link' : None,
            'data' : {
                'id': self.heart1.id,
                'userName': self.heart1.userFK.name,
                'rollingPaperName': self.heart1.paperFK.title,
                'context': self.heart1.context,
                'danger': 0,
                'createdAt': localtime(self.heart2.createdAt).strftime('%Y.%m.%d')
            }
        }

        # 응답 상태 코드 확인
        self.assertEqual(response.status_code, status.HTTP_200_OK, '상태코드가 올바르지 않습니다.')
        
        # 응답 데이터 비교
        self.assertDictEqual(response.json(), expected_data, '응답 형식이 올바르지 않습니다.')
        
        
    def test_get_heart_without_authenticated(self):
        """
            로그인하지 않은 유저는 마음을 조회할 수 없다.
            일단 보류 유저쪽 완성 안됌
        """
        pass
    
    def test_get_heart_without_invited(self):
        """
            초대 받지 않은 유저는 마음을 조회할 수 없다.
        """
        pass
    
    
    
        

class HeartWriteAPITest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # 테스트 유저 생성
        cls.receiver = User.objects.create(
            name='receiver',
            email='receiver@gmail.com',
            password='1234'
        )
        cls.host = User.objects.create(
            name='host',
            email='host@gmail.com',
            password='1234'
        )
        cls.user1 = User.objects.create(
            name='test_user1',
            email='testuser1@gmail.com',
            password='1234'
        )
        # 테스트 롤링페이퍼 생성
        cls.rolling_paper = Paper.objects.create(
            receiverFK=cls.receiver,
            hostFK=cls.host,
            receivingDate='2025-01-10',
            title='테스트 롤링페이퍼',
            description='테스트 입니다.',
            password='1234'
        )
        cls.url = reverse('heart_api')
        
    def test_create_heart(self):
        """
            새로운 마음을 생성할 수 있어야 한다.
        """
        post_data = {
            'userFK': self.user1.id,
            'paperFK': self.rolling_paper.id,
            'context': '테스트 입니다.' 
        }
        
        response = self.client.post(self.url, post_data, format='json')
        
        expected_data = {
            'status_code' : status.HTTP_201_CREATED,
            'message' : '정상적으로 생성되었습니다.',
            'code' : 'SUCCESS',
            'link' : None,
        }
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, '상태코드가 올바르지 않습니다.')
        self.assertDictEqual(response.json(), expected_data, '응답 형식이 올바르지 않습니다.')
    
    
    def test_create_heart_without_authenticated(self):
        """
            로그인하지 않은 유저는 마음을 작성할 수 없다.
            일단 보류 유저쪽 완성 안됌
        """
        pass
    
    def test_create_heart_without_invited(self):
        """
            초대 받지 않은 유저는 마음을 작성할 수 없다.
        """
        pass
    
    def test_create_heart_duplicate(self):
        """
            이미 마음을 작성한 유저는 재작성할 수 없다.
        """
        pass