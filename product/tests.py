from django.test import TestCase
from product import models


# class ProductTestCase(TestCase):

#     def setUp(self):
#         self.category = models.Category.objects.create(name="test_C")
#         models.Product.objects.create(name="test1_P", price="12000$", real_price="10000$", description="test_description", category=self.category)
#         models.Product.objects.create(name="test2_P", price="12000$", real_price="10000$", description="test_description", category=self.category)

#     def test_list_products(self):
#         response = self.client.get("/api/v1/product/products/")
#         print(response.data)