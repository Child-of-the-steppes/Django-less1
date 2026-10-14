from django.db import transaction
from rest_framework import serializers

from logistic.models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title', 'description')


class ProductPositionSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all()
    )

    class Meta:
        model = StockProduct
        fields = ('product', 'quantity', 'price')

class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ('id', 'address', 'positions')

    def create(self, validated_data):
        positions = validated_data.pop('positions')

        with transaction.atomic():
            stock = super().create(validated_data)

            for position_data in positions:
                product = position_data.pop('product')
                StockProduct.objects.create(
                    stock=stock,
                    product=product,
                    **position_data,
                )

        return stock

    def update(self, instance, validated_data):
        positions = validated_data.pop('positions', None)

        with transaction.atomic():
            stock = super().update(instance, validated_data)

            if positions is not None:
                for position_data in positions:
                    product = position_data.pop('product')
                    StockProduct.objects.update_or_create(
                        stock=stock,
                        product=product,
                        defaults=position_data,
                    )

        return stock