from .models import Announcement, User, Product, RefLink, Payment
from rest_framework import viewsets, permissions
from .serializers import UserSerializer, ProductSerializer, RefLinkSerializer, PaymentSerializer, AnnouncementSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permissions_classes = [
        permissions.AllowAny
    ]
    serializer_class = UserSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    permissions_classes = [
        permissions.AllowAny
    ]
    serializer_class = ProductSerializer


class RefLinkViewSet(viewsets.ModelViewSet):
    queryset = RefLink.objects.all()
    permissions_classes = [
        permissions.AllowAny
    ]
    serializer_class = RefLinkSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    permissions_classes = [
        permissions.AllowAny
    ]
    serializer_class = PaymentSerializer

class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.all()
    permissions_classes = [
        permissions.AllowAny
    ]
    serializer_class = AnnouncementSerializer