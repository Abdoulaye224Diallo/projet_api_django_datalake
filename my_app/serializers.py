from rest_framework import serializers
from .models import Product, APIRight

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class APIRightSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIRight
        fields = '__all__'
