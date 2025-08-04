from rest_framework import serializers
from .models import User, Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'amount', 'order_date']

class UserListSerializer(serializers.ModelSerializer):
    order_count = serializers.IntegerField()

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'order_count']

class UserDetailSerializer(serializers.ModelSerializer):
    orders = OrderSerializer(many=True, read_only=True)
    order_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'order_count', 'orders']

    def get_order_count(self, obj):
        return obj.orders.count()
