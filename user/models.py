from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    password = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=13, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    telegram_id = models.PositiveBigIntegerField(unique=True, null=True, blank=True)
    email = models.EmailField(unique=True, null=True)


    def __str__(self) -> str:
        return self.username

    class Meta:
        verbose_name = _("foydalanuvchi")
        verbose_name_plural = _("foydalanuvchilar")
        ordering = ['-created_at']


class UsersPassword(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='passwords')
    password = models.PositiveBigIntegerField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.user.username
    
    class Meta:
        verbose_name = _("foydalanuvchi paroli")
        verbose_name = _("foydalanuvchi parollari")
        ordering = ['-time']

