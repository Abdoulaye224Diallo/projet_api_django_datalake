from django.contrib import admin
from .models import Product, APIRight

# Enregistrement du modèle Product
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'description', 'created_at', 'updated_at')

# Enregistrement du modèle APIRight
@admin.register(APIRight)
class APIRightAdmin(admin.ModelAdmin):
    list_display = ('id', 'endpoint_name', 'token', 'can_access')
