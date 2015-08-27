from rest_framework import routers
from .views import ProductViewSet

smart_price_router = routers.DefaultRouter()

smart_price_router.register('smart_prices', ProductViewSet)
urlpatterns = smart_price_router.urls