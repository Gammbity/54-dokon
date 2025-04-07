from django.test import TestCase
from django.urls import reverse

from user.models import User, UsersPassword

from datetime import datetime

class UserViewTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            first_name='Ali',
            last_name='Aliyev',
            username='testuser',
            email='test@gmail.com',
            phone='+998880334626',
            password='testpassword'
        )
        self.client.login(username="testuser", password="testpassword")

    def test_get_user(self):

        response = self.client.get(f'/api/v1/user/me/')  
        self.assertEqual(response.status_code, 200)
    
    def test_registr_bot(self):

        UsersPassword.objects.create(user=self.user, password=123456, time=datetime.now())
        response = self.client.post("/api/v1/user/registration/bot/", data={"password":123456})
        self.assertEqual(response.status_code, 201)
        self.assertIn('access_token', response.data)

    def test_logout(self):
        
        response = self.client.post("/api/v1/user/logout/")
        self.assertEqual(response.status_code, 200)
    
    def test_login(self):
        user = {
            "username": "testuser", 
            "password": "testpassword"
        }
        response = self.client.post("/api/v1/user/login/", data=user)
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.data)

    def test_user_change_password_username(self):
        user = {
            "password": "testpassword",
            "username": "testuser", 
            "new_password": "testpasswordchanged"
        }
        response = self.client.post("/api/v1/user/edit/password/", data=user)
        self.assertEqual(response.status_code, 200)


class UserRegistrationTest(TestCase):
    
    def test_register_user(self):
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
        self.assertIn('access_token', response.data)


class AdminTest(TestCase):

    def setUp(self):
        self.admin = User.objects.create_superuser(username='admin', password="Qwerty123$")
        self.client.login(username='admin', password="Qwerty123$")
        self.user = User.objects.create_user(
            first_name="Ali",
            last_name="Aliyev",
            username="testuser",
            email="test@gmail.com",
            phone="+998880334626",
            password="Qwerty1234root"
        )

    def test_get_user(self):
        url = reverse('admin-users-list')
        response = self.client.get(url)
        self.assertEqual(response.data[0]['id'], 2)
        self.assertEqual(response.status_code, 200)

    def test_delete_user(self):
        url = reverse('admin-users-detail', args=[self.user.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)