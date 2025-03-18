from django.test import TestCase
from order import models
from user.models import User
from product.models import Product, Category
import json, asyncio

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
        self.product = models.Product.objects.create(
            name="test_P", 
            price=12000, 
            real_price="10000$", 
            description="test_description", 
            count=10,
            category=self.category
        )
        self.basket = models.Basket.objects.create(user=self.user)
        self.basket_item = models.BasketItem.objects.create(
            basket=self.basket, product=self.product, quantity=3, price=self.product.price * 3
        )
        self.status = models.Status.objects.create(status="Yaratildi")
        self.address = models.Address.objects.create(
            user=self.user, longitude=12, latitude=21, location="Tashkent"
        )
    def tearDown(self):
        loop = asyncio.get_event_loop()
        for task in asyncio.all_tasks(loop):
            if not task.done():
                task.cancel()
        loop.run_until_complete(asyncio.sleep(0.1))

    def test_order_create(self):
        order_data = {
            "status": self.status.id, 
            "address": {
                "longitude": 12.34,
                "latitude": 56.78,
                "location": "Tashkent"
            }
        }
        response = self.client.post(
            "/api/v1/order/order/create/",
            data=json.dumps(order_data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        self.assertIn("address", response_data)
        self.assertEqual(response_data["address"]["location"], "Tashkent")

    def test_list_orders(self):
        models.Order.objects.create(user=self.user, status=self.status, address=self.address)
        response = self.client.get("/api/v1/order/order/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["status"]["status"], "Yaratildi")
        self.assertEqual(data[0]["address"]["location"], "Tashkent")

    def test_list_basket(self):
        response = self.client.get("/api/v1/order/basket/")
        self.assertEqual(response.status_code, 200)
        response_data = response.json()

        expected_data = {
            "id": 1,
            "user_id": 1,
            "total_price": 0  
        }
        self.assertEqual(response_data["id"], expected_data["id"])
        self.assertEqual(response_data["user_id"], expected_data["user_id"])
        self.assertEqual(response_data["total_price"], expected_data["total_price"])
        
    def test_basket_item_create(self):
        quantity = 3
        basket_item = ({
            "basket": self.basket.id,
            "product": self.product.id,
            "quantity": quantity,
            "price": quantity * self.product.price
        })
        response = self.client.post("/api/v1/order/basket/item/create/", data=json.dumps(basket_item), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        self.assertEqual(response_data["product"], "test_P")  
        self.assertEqual(response_data["quantity"], quantity)  

    def test_list_address(self):
        response = self.client.get("/api/v1/order/address/")
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(len(response_data), 1)
        self.assertEqual(response_data[0]["location"], "Tashkent")
        self.assertEqual(response_data[0]["longitude"], 12)
        self.assertEqual(response_data[0]["latitude"], 21)

