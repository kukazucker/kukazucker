from rest_framework import routers
from .api import UserViewSet, ProductViewSet, RefLinkViewSet, PaymentViewSet, AnnouncementViewSet

router = routers.DefaultRouter()
router.register('api/users', UserViewSet, 'user')
router.register('api/products', ProductViewSet, 'product')
router.register('api/refs', RefLinkViewSet, 'reflink')
router.register('api/payments', PaymentViewSet, 'payment')
router.register('api/anouncements', AnnouncementViewSet, 'announcment')

urlpatterns = router.urls
