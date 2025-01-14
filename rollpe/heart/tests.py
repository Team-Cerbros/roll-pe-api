from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.utils.timezone import localtime
from urllib.parse import urlencode
from pprint import pprint


from user.models import User
from paper.models import Paper
from heart.models import Heart


"""
    마음 조회 시나리오
    
    - 공통
    1. 로그인 x => 마음목록 조회 불가능
    
    - 공개 롤링 페이퍼 => 
        2. 로그인 o => 조회 가능
        
    - 비공개 롤링 페이퍼 =>
        3. 로그인 o, 초대된 유저 x => 조회 불가능
        4. 로그인 o, 초대된 유저 o => 조회 가능
        
        
    - 인덱스 , 블러처리 필요

"""
class HeartReadAPITest(APITestCase):
    @classmethod
    def create_test_users(cls):
        """테스트 유저 생성"""
        cls.receiver = User.objects.create(
            name='receiver',
            email='receiver@gmail.com',
        )
        cls.host = User.objects.create(
            name='host',
            email='host@gmail.com',
        )
        cls.user1 = User.objects.create(
            name='test_user1',
            email='testuser1@gmail.com',
        )
        cls.user2 = User.objects.create(
            name='test_user2',
            email='testuser2@gmail.com',
        )
        cls.user1.set_password('1234')
        cls.user1.save()
        cls.user2.set_password('1234')
        cls.user2.save()

    @classmethod
    def create_test_data(cls):
        """테스트 롤링페이퍼와 마음 생성"""
        # 테스트 롤링페이퍼 생성 (공개)
        cls.public_rolling_paper = Paper.objects.create(
            receiverFK=cls.receiver,
            hostFK=cls.host,
            receivingDate='2025-01-10',
            title='공개 롤링페이퍼',
            description='테스트 입니다.',
            viewStat=True,
        )
        
        # 테스트 롤링페이퍼 생성 (비공개)
        cls.private_rolling_paper = Paper.objects.create(
            receiverFK=cls.receiver,
            hostFK=cls.host,
            receivingDate='2025-01-10',
            title='비공개 롤링페이퍼',
            description='테스트 입니다.',
            password='1234',
            viewStat=False,
        )
        
        # 롤링페이퍼로 유저 초대
        cls.private_rolling_paper.invitingUser.add(cls.user1)
        cls.private_rolling_paper.save()
        
        # 테스트 마음 생성
        cls.heart1 = Heart.objects.create(
            userFK=cls.user1,
            paperFK=cls.public_rolling_paper,
            context='공개 롤링페이퍼의 테스트 마음입니다.'
        )
        cls.heart2 = Heart.objects.create(
            userFK=cls.user2,
            paperFK=cls.public_rolling_paper,
            context='공개 롤링페이퍼의 테스트 마음입니다.'
        )
        cls.heart3 = Heart.objects.create(
            userFK=cls.user1,
            paperFK=cls.private_rolling_paper,
            context='비공개 롤링페이퍼의 테스트 마음입니다.'
        )

    @classmethod
    def setUpTestData(cls):
        """테스트 데이터 생성"""
        cls.create_test_users()
        cls.create_test_data()
        cls.url = reverse('heart_api')
        
        
    def signin(self, user):
        """
            테스트유저 로그인
        """
        signin_url = reverse('token_obtain_pair')
        signin_data = {}
        
        if user == 'user1':
            signin_data['email'] = self.user1.email
            signin_data['password'] = '1234'
        else:
            signin_data['email'] = self.user2.email
            signin_data['password'] = '1234'
            
        response = self.client.post(signin_url, signin_data)
        token = response.data.get('data')['access']
        
        # 인증 헤더 설정
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
    
    
    # 1번 시나리오
    def test_get_heart_without_authenticated(self):
        """
            로그인하지 않은 유저는 마음을 조회할 수 없다.
        """
        pcode = {'pcode': self.public_rolling_paper.code}
        url_with_params = f'{self.url}?{urlencode(pcode)}'
        response = self.client.get(url_with_params)
        
        # 응답 상태 코드 확인
        self.assertEqual(response.status_code, 401, '상태코드가 올바르지 않습니다.')
    
    
    # 2번 시나리오
    def test_get_public_heart_list(self):
        """
            공개 롤링페이퍼에 작성된 마음목록을 가져올 수 있어야 한다.
        """
        self.signin(user='user1')
        
        # API 요청
        pcode = {'pcode': self.public_rolling_paper.code}
        url_with_params = f'{self.url}?{urlencode(pcode)}'
        
        response = self.client.get(url_with_params)

        # 예상 데이터
        expected_data = [
            {
                'id': self.heart1.id,
                'userName': self.heart1.userFK.name,
                'rollingPaperName': self.heart1.paperFK.title,
                'context': self.heart1.context,
                'danger': self.heart1.danger,
                'createdAt': localtime(self.heart2.createdAt).strftime('%Y.%m.%d')
            },
            {
                'id': self.heart2.id,
                'userName': self.heart2.userFK.name,
                'rollingPaperName': self.heart2.paperFK.title,
                'context': self.heart2.context,
                'danger': self.heart2.danger,
                'createdAt': localtime(self.heart1.createdAt).strftime('%Y.%m.%d')
            }
        ]
        
        # 응답 상태 코드 확인
        self.assertEqual(response.status_code, 200, '상태코드가 올바르지 않습니다.')
        
        # 응답 데이터 비교
        self.assertListEqual(response.json()['data']['results'], expected_data, '응답 데이터가 올바르지 않습니다.')
        
    
    # 3번 시나리오
    def test_get_private_heart_list_without_invited(self):
        """
            비공개 롤링페이퍼에 작성된 마음목록을 초대되지 않은 유저는 조회할 수 없다.
        """
        self.signin(user='user2')

        # API 요청
        pcode = {'pcode': self.private_rolling_paper.code}
        url_with_params = f'{self.url}?{urlencode(pcode)}'
        
        response = self.client.get(url_with_params)
       
       # 응답 상태 코드 확인
        self.assertEqual(response.status_code, 471, '상태코드가 올바르지 않습니다.')
        
        
    # 4번 시나리오 
    def test_get_private_heart_list(self):
        """
            비공개 롤링페이퍼에 작성된 마음목록을 초대받은 유저는 조회할 수 있다.
        """
        self.signin(user='user1')
        
        # API 요청
        pcode = {'pcode': self.private_rolling_paper.code}
        url_with_params = f'{self.url}?{urlencode(pcode)}'
        
        response = self.client.get(url_with_params)
        
        # 예상 데이터
        expected_data = [
            {
                'id': self.heart3.id,
                'userName': self.heart3.userFK.name,
                'rollingPaperName': self.heart3.paperFK.title,
                'context': self.heart3.context,
                'danger': self.heart3.danger,
                'createdAt': localtime(self.heart3.createdAt).strftime('%Y.%m.%d')
            }
        ]
        
         # 응답 상태 코드 확인
        self.assertEqual(response.status_code, 200, '상태코드가 올바르지 않습니다.')
        
        # 응답 데이터 비교
        self.assertListEqual(response.json()['data']['results'], expected_data, '응답 데이터가 올바르지 않습니다.')
        
        
    def test_get_heart_detail(self):
        """
            마음 상세정보를 가져올 수 있어야 한다.
        """
        self.signin(user='user1')
        
        hcode = {'hcode': self.heart1.code}
        url_with_params = f'{self.url}?{urlencode(hcode)}'
        
        response = self.client.get(url_with_params)
        
        expected_data = {
            'id': self.heart1.id,
            'userName': self.heart1.userFK.name,
            'rollingPaperName': self.heart1.paperFK.title,
            'context': self.heart1.context,
            'danger': self.heart1.danger,
            'createdAt': localtime(self.heart2.createdAt).strftime('%Y.%m.%d')
        }

        # 응답 상태 코드 확인
        self.assertEqual(response.status_code, 200, '상태코드가 올바르지 않습니다.')
        
        # 응답 데이터 비교
        self.assertDictEqual(response.json()['data'], expected_data, '응답 데이터가 올바르지 않습니다.')
        
    

class HeartCreateAPITest(APITestCase):
    @classmethod
    def create_test_users(cls):
        """테스트 유저 생성"""
        cls.receiver = User.objects.create(
            name='receiver',
            email='receiver@gmail.com',
        )
        cls.host = User.objects.create(
            name='host',
            email='host@gmail.com',
        )
        cls.user1 = User.objects.create(
            name='test_user1',
            email='testuser1@gmail.com',
        )
        cls.user2 = User.objects.create(
            name='test_user2',
            email='testuser2@gmail.com',
        )
        cls.user1.set_password('1234')
        cls.user1.save()
        cls.user2.set_password('1234')
        cls.user2.save()

    @classmethod
    def create_test_data(cls):
        """테스트 롤링페이퍼와 마음 생성"""
        # 테스트 롤링페이퍼 생성 (공개)
        cls.public_rolling_paper = Paper.objects.create(
            receiverFK=cls.receiver,
            hostFK=cls.host,
            receivingDate='2025-01-10',
            title='공개 롤링페이퍼',
            description='테스트 입니다.',
            viewStat=True,
        )
        
        # 테스트 롤링페이퍼 생성 (비공개)
        cls.private_rolling_paper = Paper.objects.create(
            receiverFK=cls.receiver,
            hostFK=cls.host,
            receivingDate='2025-01-10',
            title='비공개 롤링페이퍼',
            description='테스트 입니다.',
            password='1234',
            viewStat=False,
        )
        
        # 롤링페이퍼로 유저 초대
        cls.private_rolling_paper.invitingUser.add(cls.user1)
        cls.private_rolling_paper.save()
        

    @classmethod
    def setUpTestData(cls):
        """테스트 데이터 생성"""
        cls.create_test_users()
        cls.create_test_data()
        cls.heart_url = reverse('heart_api')
        
        cls.public_heart_data = {
            'paperFK': cls.public_rolling_paper.id,
            'context': '마음1 테스트 입니다.',
            'index': 1
        }
        cls.private_heart_data = {
            'paperFK': cls.private_rolling_paper.id,
            'context': '마음2 테스트 입니다.',
            'index': 1
        }
    
    def signin(self, user):
        """
            테스트유저 로그인
        """
        signin_url = reverse('token_obtain_pair')
        signin_data = {}
        
        if user == 'user1':
            signin_data['email'] = self.user1.email
            signin_data['password'] = '1234'
        else:
            signin_data['email'] = self.user2.email
            signin_data['password'] = '1234'
            
        response = self.client.post(signin_url, signin_data)
        token = response.data.get('data')['access']
        
        # 인증 헤더 설정
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
    
        
    def test_create_heart_without_authenticated(self):
        """
            로그인하지 않은 유저는 마음을 작성할 수 없다.
        """
        response = self.client.post(self.heart_url, self.public_heart_data, format='json')
        
        # 응답 상태 코드 확인
        self.assertEqual(response.status_code, 401, '상태코드가 올바르지 않습니다.')
        
        
    def test_create_heart_without_invited(self):
        """
            초대 받지 않은 유저는 마음을 작성할 수 없다.
        """
        self.signin('user2')
        response = self.client.post(self.heart_url, self.private_heart_data, format='json')
        
        # 응답 상태 코드 확인
        self.assertEqual(response.status_code, 471, '상태코드가 올바르지 않습니다.')
    
    
    def test_create_heart(self):
        """
            새로운 마음을 생성할 수 있어야 한다.
        """
        self.signin('user1')
        private_response = self.client.post(self.heart_url, self.private_heart_data, format='json')
        public_response = self.client.post(self.heart_url, self.public_heart_data, format='json')
        
        # 응답 상태 코드 확인
        self.assertEqual(private_response.status_code, 201, '상태코드가 올바르지 않습니다.')
        
        # 응답 상태 코드 확인
        self.assertEqual(public_response.status_code, 201, '상태코드가 올바르지 않습니다.')
    
    
    def test_create_heart_duplicate(self):
        """
            이미 마음을 작성한 유저는 재작성할 수 없다.
        """
        self.signin('user1')
        self.client.post(self.heart_url, self.private_heart_data, format='json')
        
        # 재작성 요청
        response = self.client.post(self.heart_url, self.private_heart_data, format='json')
    
        self.assertEqual(response.status_code, 482, '상태코드가 올바르지 않습니다.')
    
    
    
