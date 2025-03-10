# accounts/views.py
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ShieldbotUser
from rest_framework_simplejwt.tokens import RefreshToken
from api.serializers import UserSerializer
class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'User registered successfully',
                'user': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            # Log the user in to create a session
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'User logged in successfully',
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class UserLogoutView(APIView):
    def post(self, request):
        # For JWT, logout is often handled client-side by deleting tokens.
        # Optionally, you can implement token blacklisting if required.
        return Response({'message': 'User logged out successfully.'}, status=status.HTTP_200_OK)

class PasswordResetView(APIView):
    def post(self, request):
        email = request.data.get('email')
        try:
            user = ShieldbotUser.objects.get(email=email)
            # In production, send a password reset email or token.
            return Response({'message': 'Password reset link has been sent.'}, status=status.HTTP_200_OK)
        except ShieldbotUser.DoesNotExist:
            return Response({'error': 'User with provided email does not exist.'}, status=status.HTTP_404_NOT_FOUND)

class VerifyTokenView(APIView):
    def get(self, request):
        # With JWTAuthentication, if the token is invalid, the request won't reach this point.
        return Response({'message': 'Token is valid.'}, status=status.HTTP_200_OK)

class RefreshTokenView(APIView):
    def post(self, request):
        # You can either delegate to SimpleJWT’s built-in view or implement your own logic.
        from rest_framework_simplejwt.views import TokenRefreshView as SimpleJWTTokenRefreshView
        view = SimpleJWTTokenRefreshView.as_view()
        # Note: Passing request._request to the underlying view
        return view(request._request)
