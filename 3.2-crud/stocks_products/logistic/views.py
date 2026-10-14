from django.db.models import Q
from rest_framework import filters
from rest_framework.viewsets import ModelViewSet

from logistic.models import Product, Stock
from logistic.serializers import ProductSerializer, StockSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title', 'description')


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

    def get_queryset(self):
        queryset = Stock.objects.prefetch_related(
            'positions__product'
        )

        product_id = self.request.query_params.get('products')
        if product_id:
            queryset = queryset.filter(products__id=product_id)

        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(products__title__icontains=search)
                | Q(products__description__icontains=search)
            )

        return queryset.distinct()