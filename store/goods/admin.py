from django.contrib import admin

# Register your models here.
from .models import Categories, Products


admin.site.register(Categories)
admin.site.register(Products)
