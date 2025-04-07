from django.test import TestCase
from . import models
from user.models import User
from product.models import Product, Category
import json, asyncio
from django.urls import reverse
from . import serializers

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

    # ORDER

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
        self.assertEqual(response.data["message"], "Buyurtma yaratildi!")
        self.assertEqual(response.data['order_id'], 1)

    def test_list_orders(self):
        models.Order.objects.create(user=self.user, status=self.status, address=self.address)
        response = self.client.get("/api/v1/order/order/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["status"]["status"], "Yaratildi")
        self.assertEqual(data[0]["address"]["location"], "Tashkent")


    # BASKET

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

    # ADDRESS 

    def test_list_address(self):
        response = self.client.get("/api/v1/order/address/")
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(len(response_data), 1)
        self.assertEqual(response_data[0]["location"], "Tashkent")
        self.assertEqual(response_data[0]["longitude"], 12)
        self.assertEqual(response_data[0]["latitude"], 21)

class OrderAdminTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username='user1', password='12345')
        self.client.login(username='user1', password='12345')

        self.category = Category.objects.create(name='Electronics')
        self.product = Product.objects.create(name='Laptop', price=1200, count=5, category=self.category)

        self.basket = models.Basket.objects.create(user=self.user)
        self.basket_item = models.BasketItem.objects.create(basket=self.basket, product=self.product, quantity=2)
        
        self.status = models.Status.objects.create(status="Yaratildi")
        self.address = models.Address.objects.create(
            user=self.user, longitude=12, latitude=21, location="Tashkent"
        )
        self.order = models.Order.objects.create(user=self.user, address=self.address, total_price=0, status=self.status)
        self.order_item = models.OrderItem.objects.create(order=self.order, product=self.product, quantity=2, price=2400)

    # ORDER
    def test_order_detail(self):
        url = reverse('admin-order-detail', args=[self.order.id])
        response = self.client.get(url)
        self.assertEqual(response.data['user'], 'user1')
        self.assertEqual(response.status_code, 200)

    def test_order_update(self):
        url = reverse('admin-order-detail', args=[self.order.id])
        status = models.Status.objects.create(status="Jarayonda")
        response = self.client.patch(url, data=json.dumps({"status": status.id}), content_type="application/json")
        self.assertEqual(response.data['status'], 2)
        self.assertEqual(response.status_code, 200)

    def test_order_delete(self):
        url = reverse('admin-order-detail', args=[self.order.id])
        response = self.client.delete(url)
        print(response.data)
        self.assertEqual(response.status_code, 204)

    # ORDER ITEM
    def test_orderitem_detail(self):
        url = reverse('admin-order-item-detail', args=[self.order_item.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_orderitem_update(self):
        url = reverse('admin-order-item-detail', args=[self.order_item.id])
        data = {"quantity": 3, "price": 3600}
        response = self.client.patch(url, data, content_type="application/json")
        self.assertEqual(response.data['quantity'], 3)
        self.assertEqual(response.status_code, 200)

    def test_orderitem_delete(self):
        url = reverse('admin-order-item-detail', args=[self.order_item.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

    # BASKET
    def test_basket_detail(self):
        url = reverse('admin-basket-detail', args=[self.basket.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_basket_delete(self):
        url = reverse('admin-basket-detail', args=[self.basket.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

    # BASKET ITEM
    def test_basketitem_detail(self):
        url = reverse('admin-basket-item-detail', args=[self.basket_item.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_basketitem_update(self):
        url = reverse('admin-basket-item-detail', args=[self.basket_item.id])
        data = {"quantity": 5}
        response = self.client.patch(url, data, content_type="application/json")
        print(response.data)
        self.assertEqual(response.data['quantity'], 5)
        self.assertEqual(response.status_code, 200)

    def test_basketitem_delete(self):
        url = reverse('admin-basket-item-detail', args=[self.basket_item.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)