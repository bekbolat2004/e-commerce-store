from django.contrib import admin
from .models import Basket
# Register your models here.

class BasketTabAdmin(admin.TabularInline):
    model = Basket
    fields = 'product', 'quantity', 'created_timestamp'
    search_fields = 'product', 'quantity', 'created_timestamp'
    readonly_fields = ('created_timestamp',)
    extra = 1
@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ['user_display', 'product_display', 'quantity', 'created_timestamp',]
    list_filter = ['product__name', 'quantity', 'created_timestamp',]

    def user_display(self, obj):
        if obj.user:
            return str(obj.user)
        return "Anonymous User"

    def product_display(self, obj):
        return str(obj.product.name)
