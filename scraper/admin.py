from django.contrib import admin
from .models import Category, Site, ParseTask, Product

admin.site.register(Category)
admin.site.register(Site)
admin.site.register(ParseTask)
admin.site.register(Product)