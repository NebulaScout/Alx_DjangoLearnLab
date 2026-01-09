from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, get_user_model

from  .serializers import (
    UserLoginSerializer,
    UserProfileSerializer,
    UserRegistrationSerializer,
)

UserModel = get_user_model()

class UserRegistrationView(generics.CreateAPIView):
    """API endpoint for registering new users"""

    queryset = UserModel.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token = Token.objects.get(user=user)

        response_data = {
            'user': {
                'id' : user.id,
                'username': user.username,
                'email': user.email,
            },
            'token': token.key,
            'message': 'Account created successfully'
        }

        return Response(response_data, status=status.HTTP_201_CREATED)
    
class UserLoginView(APIView):
    """API endpoint for user authentication and token retrieval"""
    
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(username=username, password=password)

        if user is None:
            return Response(
                {'error': 'Invalid username or password'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
        })
        
class UserProfileView(generics.RetrieveUpdateAPIView):
    """API endpoint for viewing and updating user profile"""

    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user