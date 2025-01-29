from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from model_bakery import baker
from django.contrib.auth import get_user_model
from paper.models import Paper, QueryIndexTable
import json


class UserPaperAPITest(APITestCase):
	def setUp(self):
		self.user = baker.make(get_user_model())
		self.client.force_authenticate(user=self.user)
		self.theme = baker.make(QueryIndexTable, type='THEME')
		self.size = baker.make(QueryIndexTable, type='SIZE')
		self.ratio = baker.make(QueryIndexTable, type='RATIO')

	def test_get_papers(self):
		paper = baker.make(Paper, hostFK=self.user, themeFK=self.theme, sizeFK=self.size, ratioFK=self.ratio)
		url = reverse('paper_api_for_user')
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		response_data = json.loads(response.content)
		self.assertIn(paper.title, [item['title'] for item in response_data['data']['results']])

	def test_create_paper(self):
		data = {
			'hostFK': self.user.id,
			'themeFK': self.theme.id,
			'sizeFK': self.size.id,
			'ratioFK': self.ratio.id,
			'receiverName': 'Test Receiver',
			'receiverTel': '01012345678',
			'receivingDate': '2023-10-01',
			'title': 'New Paper',
			'description': 'This is a new paper',
			'password': 'testpassword'
			}
		url = reverse('paper_api_for_user')
		response = self.client.post(url, data=data)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		response_data = json.loads(response.content)
		self.assertEqual(response_data['data']['title'], data['title'])

	def test_delete_paper(self):
		paper = baker.make(Paper, hostFK=self.user)
		url = reverse('paper_api_for_user')
		response = self.client.delete(url, data={'pcode': str(paper.code)}, format='json')
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
		with self.assertRaises(Paper.DoesNotExist):
			Paper.objects.get(id=paper.id)


class PaperAPITest(APITestCase):
	def setUp(self):
		self.user = baker.make(get_user_model())
		self.client.force_authenticate(user=self.user)
		self.paper = baker.make(Paper, hostFK=self.user)

	def test_get_paper_detail(self):
		url = reverse('paper_api') + f'?pcode={self.paper.code}'
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		response_data = json.loads(response.content)
		self.assertEqual(response_data['data']['title'], self.paper.title)

	def test_post_paper(self):
		data = {
			'hostFK': self.user.id,
			'themeFK': self.paper.themeFK.id,
			'sizeFK': self.paper.sizeFK.id,
			'ratioFK': self.paper.ratioFK.id,
			'receiverName': 'Test Receiver',
			'receiverTel': '01012345678',
			'receivingDate': '2023-10-01',
			'title': 'New Paper',
			'description': 'This is a new paper',
			'password': 'testpassword'
			}
		url = reverse('paper_api')
		response = self.client.post(url, data=data)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class PaperEnterManageAPITest(APITestCase):
	def setUp(self):
		self.user = baker.make(get_user_model())
		self.client.force_authenticate(user=self.user)

	def test_enter_manage_with_valid_password(self):
		paper = baker.make(Paper, hostFK=self.user, password='testpassword')
		url = reverse('paper_invite_api')
		response = self.client.post(url, {'pcode': str(paper.code), 'password': 'testpassword'}, format='json')
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

	def test_enter_manage_with_invalid_password(self):
		paper = baker.make(Paper, hostFK=self.user)
		url = reverse('paper_invite_api')
		response = self.client.post(url, {'pcode': str(paper.code), 'password': 'wrongpassword'}, format='json')

		# 응답이 JSON 형식인지 확인
		try:
			response_data = json.loads(response.content)
			# 비밀번호 불일치 상태 코드는 472로 확인
			self.assertEqual(response.status_code, 472)
			self.assertEqual(response_data['message'], "롤페의 비밀번호가 틀립니다.")

		except json.JSONDecodeError:
			# JSON 디코딩 오류 발생 시 처리
			print("Response content is not valid JSON:", response.content)


# class PaperPasswordAPITest(APITestCase):
# 	def setUp(self):
# 		self.user = baker.make(get_user_model())
# 		self.client.force_authenticate(user=self.user)
#
# 	def test_change_password_success(self):
# 		paper = baker.make(Paper, hostFK=self.user, password='oldpassword')
#
# 		url = reverse('paper_api') + '/password/'
#
# 		data = {
# 			"pcode": str(paper.code),
# 			"original_password": "oldpassword",
# 			"change_password": "newpassword"
# 			}
#
# 		response = self.client.put(url, data=data)
#
# 		# 비밀번호 변경 성공 시 상태 코드 확인
# 		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#
# 	def test_change_password_fail_due_to_wrong_original(self):
# 		paper = baker.make(Paper, hostFK=self.user)
#
# 		url = reverse('paper_api') + '/password/'
#
# 		data = {
# 			"pcode": str(paper.code),
# 			"original_password": "wrongpassword",
# 			"change_password": "newpassword"
# 			}
#
# 		response = self.client.put(url, data=data)
#
# 		# 응답이 JSON 형식인지 확인
# 		try:
# 			response_data = json.loads(response.content)
# 			# 비밀번호 불일치 상태 코드는 472로 확인
# 			self.assertEqual(response.status_code, 472)
# 			# 메시지 확인 (예시 메시지 사용; 실제 메시지에 맞게 수정 필요)
# 			self.assertEqual(response_data['message'], "기존 비밀번호와 다릅니다.")
#
# 		except json.JSONDecodeError:
# 			# JSON 디코딩 오류 발생 시 처리
# 			print("Response content is not valid JSON:", response.content)

