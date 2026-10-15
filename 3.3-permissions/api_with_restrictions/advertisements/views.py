from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement
from advertisements.permissions import IsAdvertisementCreator
from advertisements.serializers import AdvertisementSerializer


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AdvertisementFilter

    def get_permissions(self):
        """Получение прав для действий."""

        if self.action == "create":
            permission_classes = (IsAuthenticated,)
        elif self.action in ("update", "partial_update", "destroy"):
            permission_classes = (IsAuthenticated, IsAdvertisementCreator)
        else:
            permission_classes = (AllowAny,)

        return [permission() for permission in permission_classes]