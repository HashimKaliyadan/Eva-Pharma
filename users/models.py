from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    phone_number = models.CharField(max_length=12)
    is_manager= models.BooleanField('Is manager', default=False)
    is_customer = models.BooleanField('Is customer', default=False)


    class Meta:
        db_table = 'user_user'
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ["-id"]

    def __str__(self):
        return self.username
