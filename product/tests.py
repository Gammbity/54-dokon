from django.test import TestCase
from product import models
import unittest
from unittest.mock import patch
import io
from product.tasks import schedule_tasks

class ProductTestCase(TestCase):

    def setUp(self):
        self.category = models.Category.objects.create(name="test_C")
        models.Product.objects.create(name="test1_P", price=12000, real_price="10000$", description="test_description", category=self.category)
        models.Product.objects.create(name="test2_P", price=12000, real_price="10000$", description="test_description", category=self.category)

    def test_list_products(self):
        response = self.client.get("/api/v1/product/products/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("test1_P", response.data[0]['name'])
        self.assertIn("test2_P", response.data[1]['name'])

    def test_get_product(self):
        response = self.client.get(f"/api/v1/product/product/{2}/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("test2_P", response.data['name'])

class CategoryTestCase(TestCase):

    def setUp(self):
        models.Category.objects.create(name="test1")
        models.Category.objects.create(name="test2")

    def test_categories(self):
        response = self.client.get("/api/v1/product/categories/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("test1", response.data[0]['name'])
        self.assertIn("test2", response.data[1]['name'])

    def test_get_category(self):
        response = self.client.get(f"/api/v1/product/category/{1}/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("test1", response.data['name'])
