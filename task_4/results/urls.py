from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MedicalImageResultViewSet

router = DefaultRouter()
router.register(r'elements', MedicalImageResultViewSet)

urlpatterns = [
    path('', include(router.urls)),
]