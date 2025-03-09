from django.shortcuts import render
from rest_framework import generics, permissions
from tests.models import Test
from api.serializers import TestSerializer
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.http import require_GET
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class TestListAPIView(APIView):
    permission_classes = [IsAuthenticated]


    def get(self, request, *args, **kwargs):
        available_tests = [
            {"name": "DDOS Attack", "description": "Simulate a distributed denial-of-service attack."},
            {"name": "Brute Force Attack", "description": "Attempt to crack passwords by brute force."},
            {"name": "Port Scan", "description": "Scan the target for open ports."},
            {"name": "API-Based Test", "description": "Perform a test via external API integration."},
        ]
        return Response({"available_tests": available_tests}, status=status.HTTP_200_OK)


class TestListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = TestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Test.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@require_GET
def csrf_token_view(request):
    return JsonResponse({'csrfToken': get_token(request)})
