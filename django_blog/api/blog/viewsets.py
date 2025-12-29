from rest_framework import (
    permissions,
    status,
    viewsets,
)
from django.contrib.auth.models import User

from .serializers import RegistrationSerializer

class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    