from django.test import TestCase
from product import models
from user.models import User
import json

# class ProductTestCase(TestCase):

#     def setUp(self):
#         self.category = models.Category.objects.create(name="test_C")
#         self.product = models.Product.objects.create(name="test1", price=12000, real_price="10000$", description="test_description", category=self.category)
        
#     def test_list_products(self):
#         response = self.client.get("/api/v1/product/products/")
#         self.assertEqual(response.status_code, 200)
#         self.assertIn("test1", response.data[0]['name'])

#     def test_get_product(self):
#         response = self.client.get(f"/api/v1/product/product/{self.product.name}/")
#         self.assertEqual(response.status_code, 200)
#         self.assertIn("test1", response.data['name'])

class CategoryTestCase(TestCase):

    def setUp(self):
        self.category = models.Category.objects.create(name="test1")

    # def test_categories(self):
    #     response = self.client.get("/api/v1/product/categories/")
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn("test1", response.data[0]['name'])

    # def test_get_category(self):
    #     response = self.client.get(f"/api/v1/product/category/{self.category.name}/")
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn("test1", response.data['name'])

    def test_create_category(self):
        category = {
            "image": "../../../../home/abduboriyxoja/Pictures/my.jpg",
            "name": "Electro",
        }

        response = self.client.post("/api/v1/product/admin/category/create/", data=json.dumps(category), content_type="application/json")
        print(response)