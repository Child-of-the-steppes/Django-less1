from rest_framework import generics

from .models import Measurement, Sensor
from .serializers import (
    MeasurementCreateSerializer,
    SensorDetailSerializer,
    SensorSerializer,
)


class SensorListCreateView(generics.ListCreateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer


class SensorDetailView(generics.RetrieveUpdateAPIView):
    queryset = Sensor.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SensorDetailSerializer
        return SensorSerializer


class MeasurementCreateView(generics.CreateAPIView):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementCreateSerializer