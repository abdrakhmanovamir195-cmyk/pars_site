from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)  # носки, трусы и т.д.

    def __str__(self):
        return self.name


class Site(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField()
    parser_key = models.CharField(max_length=50)
    category = models.OneToOneField(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='site'
    )

    def __str__(self):
        return self.name


class ParseTask(models.Model):
    STATUS = [
        ('pending', 'Ожидает'),
        ('running', 'Выполняется'),
        ('done', 'Готово'),
        ('error', 'Ошибка'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sites = models.ManyToManyField(Site)
    categories = models.ManyToManyField(Category)
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Задача #{self.id} — {self.status}"


class Product(models.Model):
    task = models.ForeignKey(ParseTask, on_delete=models.CASCADE, related_name='products')
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.CharField(max_length=50)
    url_img = models.URLField(blank=True)

    def __str__(self):
        return self.name