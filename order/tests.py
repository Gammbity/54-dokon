from django.test import TestCase
from order.models import Order, Basket
from user.models import User
from product.models import Product, Category

class OrderTestCase(TestCase):

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
        self.category = Category.objects.create(name="test_C")
        self.product = Product.objects.create(
            name="test_P", 
            price=12000, 
            real_price="10000$", 
            description="test_description", 
            category=self.category
        )
       

    def test_list_orders(self):
        Order.objects.create(
            user = self.user,
            longitude = 12.342,
            latitude = 45.654,
            location = "Uzbekistan, Tashkent",
        )
       
        response = self.client.get("/api/v1/order/orders/")
        self.assertEqual(response.status_code, 200)



    def test_order_create(self):
        order = {
            "user": self.user.id,
            "longitude": 12.123,
            "latitude": 43.654,
            "location": "Uzbekistan/Tashkent",
            "order_item": [
                {
                    "product": self.product.id,
                    "price": 12000,
                    "quantity": 3
                }
            ]
        }
        response = self.client.post("/api/v1/order/order/create/", data=order, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('order_item', response.data)
        self.assertEqual(response.data['location'], "Uzbekistan/Tashkent")
        self.assertEqual(response.data['order_item'][0]['product'], 1)


class BasketTestCase(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            first_name='Ali',
            last_name='Aliyev',
            username='testuser',
            email='test@gmail.com',
            phone='+998880334626',
            password='testpassword'
        )
        self.client.login(username="testuser", password="testpassword")
        self.category = Category.objects.create(name="test_C")
        self.product = Product.objects.create(
            name="test_P", 
            price=12000, 
            real_price="10000$", 
            description="test_description", 
            category=self.category
        )
        
    def test_basket_get(self):
        Basket.objects.create(
            user=self.user, 
            product=self.product, 
            )
        
        response = self.client.get("/api/v1/order/basket/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("test_P", response.data[0]['product']['name'])
    
    def test_basket_create(self):
        basket = {
            'user':self.user.id,
            'product':self.product.id
        }
        response = self.client.post("/api/v1/order/basket/create/", data=basket)
        self.assertEqual(response.status_code, 201)
        self.assertIn('product', response.data)