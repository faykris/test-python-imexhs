from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import MedicalImageResult
from .serializers import MedicalImageResultSerializer


class MedicalImageResultViewSet(viewsets.ModelViewSet):
    queryset = MedicalImageResult.objects.all()
    serializer_class = MedicalImageResultSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if 'device_name' in request.data:
            instance.device_name = request.data['device_name']
            instance.raw_data['deviceName'] = request.data['device_name']
        if 'id' in request.data:
            instance.id = request.data['id']

        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
