from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from user.models import User
from paper.models import Paper  # Paper 모델 임포트

class UserPaperAPITestCase(APITestCase):
    def setUp(self):
        # 테스트용 사용자 생성
        self.user1 = User.objects.create_user(name="user1", email="user1@test.com", password="password1", is_active=True)
        self.user2 = User.objects.create_user(name="user2", email="user2@test.com", password="password2", is_active=True)
        self.user3 = User.objects.create_user(name="user3", email="user3@test.com", password="password3", is_active=True)

        # 테스트용 Paper 생성
        self.paper1 = Paper.objects.create(
            hostFK=self.user1,
            receiverFK=self.user2,
            receiverName="Receiver 1",
            receiverTel="01012345678",
            receivingDate="2023-12-01",
            title="Paper 1",
            description="Description for Paper 1"
        )
        self.paper2 = Paper.objects.create(
            hostFK=self.user1,
            receiverFK=self.user3,
            receiverName="Receiver 2",
            receiverTel="01098765432",
            receivingDate="2023-12-02",
            title="Paper 2",
            description="Description for Paper 2"
        )

        # invitingUser에 추가
        self.paper1.invitingUser.add(self.user3)
        self.paper2.invitingUser.add(self.user2)

        # API URL 설정
        self.inviting_user_papers_url = reverse("myid_in_invate_rollpe")  # 내 ID가 invitingUser에 속한 Papers
        self.receiver_papers_url = reverse("receiver_is_me")  # receiverFK_id가 내 ID인 Papers

        # 인증 설정
        self.client.force_authenticate(user=self.user3)

    def test_get_papers_where_inviting_user(self):
        """
        내 ID가 invitingUser에 속한 Papers 목록과 갯수 가져오기 테스트
        """
        response = self.client.get(self.inviting_user_papers_url)
        
        # 응답 확인
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 데이터 확인 (user3는 paper1의 invitingUser로 추가됨)
        self.assertEqual(len(response.data.get("data").get("papers")), 1)  # paper1만 포함됨
        self.assertEqual(response.data.get("data").get("count"), 1)
    
    def test_get_papers_where_receiver(self):
        """
        receiverFK_id가 내 ID인 Papers 목록과 갯수 가져오기 테스트
        """
        response = self.client.get(self.receiver_papers_url)
        
        # 응답 확인
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 데이터 확인 (user3는 paper2의 receiverFK임)
        self.assertEqual(len(response.data.get("data").get("papers")), 1)  # paper1만 포함됨
        self.assertEqual(response.data.get("data").get("count"), 1)
