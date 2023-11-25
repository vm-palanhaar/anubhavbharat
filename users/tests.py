from rest_framework.test import APIRequestFactory
from django.test import TestCase

from users import models as UserMdl
from users import serializers as UserSrl
from users.common.api.v1 import api_views as UserApiV1

class UserSignupTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = UserApiV1.UserSignupApi.as_view()
        self.serializer = UserSrl.UserSignupSerializer()
        self.apiv1 = '/api/user/v1/signup'

    @classmethod
    def setUpTestData(cls):
        user = UserMdl.User.objects.create(
            first_name = 'Test',
            last_name = 'User_1',
            contact_no ='0000000000',
            username = 'test_user_1',
            email = 'test_user_1@palanhaar.in'
        )
        user.set_password('adminadmin')
        user.save()

    def test_user_signup_success(self):
        request = self.factory.post(
            self.apiv1,
            {
                'first_name': 'Test',
                'last_name' : 'User',
                'contact_no' :'0000000000',
                'username' : 'test_user',
                'email' : 'test_user@palanhaar.in',
                'password' : 'adminadmin',
            },
        )
        response = self.view(request)
        self.assertEqual(response.status_code, 201, response.data)

    def test_user_signup_failed(self):
        request = self.factory.post(
            self.apiv1,
            {
                'first_name': 'Test',
                'last_name' : 'User_1',
                'contact_no' :'0000000000',
                'username' : 'test_user_1',
                'email' : 'test_user_1@palanhaar.in',
                'password' : 'adminadmin',
            },
        )
        response = self.view(request)
        self.assertEqual(response.status_code, 400, response.data)