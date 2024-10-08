from django.test import TestCase
from user.models import User


class MeViewTest(TestCase):

    def setUp(self): 
        self.user = User.objects.create_user(
            first_name='Ali',
            last_name='Aliyev',
            username='testuser',
            email='test@gmail.com',
            phone='+998880334626',
            password='testpassword'
        )

    def test_get_user(self):
        self.client.login(username=self.user.username, password=self.user.password)
        response = self.client.get(f'/api/v1/user/me/')  
        self.assertEqual(response.status_code, 200)
        print(response.data)

    # def test_registr_user(self):
    #     user = {
    #         "first_name":"Ali",
    #         "last_name":"Aliyev",
    #         "username":"testuser",
    #         "email":"test@gmail.com",
    #         "phone":"+998880334626",
    #         "password":"testpassword"
    #     }
    #     respone = self.client.post("/api/v1/user/registration/", data=user)
    #     self.assertEqual(respone.status_code, 201)