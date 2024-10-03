from django.db import models
from django.contrib.auth.models import AbstractUser

from django.utils.translation import gettext_lazy as _

from common.models import BaseModel

class User(AbstractUser, BaseModel):
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=13, blank=True)

    def __str__(self) -> str:
        return self.get_full_name()

    class Meta:
        verbose_name = _("Foydalanuvchi")
        verbose_name_plural = _("Foydalanuvchilar")

