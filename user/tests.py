from django.test import TestCase
from user.models import User


class UserViewTest(TestCase):

    def test_get_user(self):
        self.user = User.objects.create_user(
            first_name='Ali',
            last_name='Aliyev',
            username='testuser',
            email='test@gmail.com',
            phone='+998880334626',
            password='testpassword'
        )
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(f'/api/v1/user/me/')  
        self.assertEqual(response.status_code, 200)

    def test_registr_user(self):
        user = {
            "first_name":"Ali",
            "last_name":"Aliyev",
            "username":"testuser",
            "email":"test@gmail.com",
            "phone":"+998880334626",
            "password":"Qwerty1234root"
        }
        response = self.client.post("/api/v1/user/registration/", data=user) 
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['message'], "Registration muvaffaqiyatli amalga oshirildi")
        self.assertIn('access_token', response.data)