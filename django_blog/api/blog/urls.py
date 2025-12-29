from rest_framework.routers import DefaultRouter

from .viewsets import RegistrationViewSet

router = DefaultRouter()
router.register(r'register', RegistrationViewSet, basename='api-register-user')

urlpatterns = router.urls