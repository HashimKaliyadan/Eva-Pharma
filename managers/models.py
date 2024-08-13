from django.db import models

from users.models import User


class Manager(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'manager_manager'
        verbose_name = 'manager'
        verbose_name_plural = 'managers'
        ordering = ["-id"]

    def __str__(self):
        return self.user.username
    

class Category(models.Model):
    name=models.CharField(max_length=25)
    image=models.ImageField(upload_to="category")

    class Meta:
        db_table = 'manager_category'
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        ordering = ["-id"]

    def __str__(self):
        return self.name


class Product(models.Model):
    name=models.CharField(max_length=25)
    description=models.TextField()
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    price=models.FloatField()
    image=models.ImageField(upload_to="products")
    is_stock=models.BooleanField(default=True)


    class Meta:
        db_table = 'manager_product'
        verbose_name = 'product'
        verbose_name_plural = 'products'
        ordering = ["-id"]

    def __str__(self):
        return self.name
