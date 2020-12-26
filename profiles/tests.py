import json

from django.contrib.auth.models import User 
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from profiles.api.serializers import ProfileSerializer,ProfileStatusSerializer
from profiles.models import Profile,ProfileStatus

class RegistrationTestCase(APITestCase):

	def test_registration(self):
		data = {"username":"testcase","email":"test@localhost.com",
				"password1":"some_stromg_psw","password2":"some_stromg_psw"}
		response = self.client.post("/api/rest-auth/registration/",data)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class ProfileViewSetTestCase(APITestCase):

	list_url = reverse('profile-list')

	def setUp(self):
		self.user = User.objects.create_user(username='davinci',
											 password='some-very-strn')
		self.token = Token.objects.create(user=self.user)
		self.api_authentication()

	def api_authentication(self):
		self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

	def test_profile_list_authenticated(self):
		response = self.client.get('/api/profiles/')
		self.assertEqual(response.status_code,status.HTTP_200_OK)

	def test_profile_list_un_authenticated(self):
		self.client.force_authenticate(user=None)
		response = self.client.get(self.list_url)
		self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

	def test_profile_detail_retrieve(self):
		response = self.client.get(reverse("profile-detail", kwargs={"pk":1}))
		self.assertEqual(response.status_code,status.HTTP_200_OK)
		self.assertEqual(response.data['user'],'davinci')

	def test_profile_update_by_owner(self):
		response = self.client.put(reverse('profile-detail', kwargs={"pk":1}),
									{'city':'dang','bio':'dang'})
		self.assertEqual(json.loads(response.content),
							{'id':1,'user':'davinci','bio':'dang','city':'dang','avatar':None})

	def test_profile_update_by_random_user(self):
		random_user = User.objects.create_user(username='random',
											 password='some-verstrn')
		self.client.force_authenticate(user=random_user)
		response = self.client.put(reverse('profile-detail', kwargs={"pk":1}),
									{'bio':'hacked'})
		self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

class ProfileStatusViewSetTestCase(APITestCase):

	list_url = reverse('status-list')

	def setUp(self):
		self.user = User.objects.create_user(username='davinci',
											 password='some-very-strn')
		self.status = ProfileStatus.objects.create(user_profile=self.user.profile,
												   status_content='status test')
		self.token = Token.objects.create(user=self.user)
		self.api_authentication()

	def api_authentication(self):
		self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

	def test_status_list_authenticated(self):
		response = self.client.get(self.list_url)
		self.assertEqual(response.status_code,status.HTTP_200_OK)

	def test_status_list_un_authenticated(self):
		self.client.force_authenticate(user=None)
		response = self.client.get(self.list_url)
		self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)