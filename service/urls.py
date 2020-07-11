from django.urls import path, include

from rest_framework import routers

from service.views import RestaurantViewSet, ReviewViewSet, LicenseViewSet


router = routers.DefaultRouter()
router.register(r'restaurant', RestaurantViewSet)
router.register(r'review', ReviewViewSet)
router.register(r'license', LicenseViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]