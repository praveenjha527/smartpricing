from rest_framework import routers
from .views import ProductViewSet, SuggestedPricesViewSet

smart_price_router = routers.DefaultRouter()

smart_price_router.register('smart_prices', ProductViewSet)
smart_price_router.register('suggested_prices', SuggestedPricesViewSet)
urlpatterns = smart_price_router.urls