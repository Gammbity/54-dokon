from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor_uploader.fields import RichTextUploadingField
    

class Category(models.Model):
    image = models.ImageField(upload_to='category/')
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = _("kategoriya")
        verbose_name_plural = _("kategoriyalar")

class Product(models.Model):
    name = models.CharField(max_length=255)
    real_price = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    description = RichTextUploadingField()
    count = models.PositiveBigIntegerField(default=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = _("mahsulot")
        verbose_name_plural = _("mahsulotlar")

class ProductImage(models.Model):
    image = models.ImageField(upload_to='product/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_image')

    def __str__(self) -> str:
        return self.image.url
    
    class Meta:
        verbose_name = _("mahsulot rasmi")
        verbose_name_plural = _("mahsulot rasmlari")