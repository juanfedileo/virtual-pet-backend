from rest_framework import serializers
from .models import Orders
from products.models import Product

class OrderSerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Product.objects.all()
    )

    class Meta:
        model = Orders
        fields = ['id', 'client', 'employee', 'products', 'status', 'created_at']
    
    def validate(self, data):
        client = data.get('client')
        employee = data.get('employee')

        if client.role != 'cliente':
            raise serializers.ValidationError({"client": "El usuario asignado como cliente no tiene el rol 'cliente'."})

        if employee.role != 'empleado':
            raise serializers.ValidationError({"employee": "El usuario asignado como empleado no tiene el rol 'empleado'."})

        return data