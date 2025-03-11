from rest_framework import serializers
from ..models.Order import Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'table_number', 'items', 'total_price', 'status']