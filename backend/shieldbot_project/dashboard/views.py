from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from accounts.models import ShieldbotUser
from tests.models import Test
import logging

logger = logging.getLogger(__name__)

# Create your views here.

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            # Get user's tests
            tests = Test.objects.filter(user=user).order_by('-start_time')
            
            # Count running tests
            running_count = Test.objects.filter(
                user=user,
                status__in=['Pending', 'Running']
            ).count()
            
            # Prepare response
            dashboard_data = {
                'username': user.username,
                'profile_picture': user.profile_picture.url if user.profile_picture else None,
                'total_tests': tests.count(),
                'running_tests': running_count,
                'tests': [{
                    'id': test.id,
                    'test_name': test.test_name,
                    'base_url': test.base_url,
                    'status': test.status,
                    'start_time': test.start_time,
                    'end_time': test.end_time
                } for test in tests]
            }
            
            return Response(dashboard_data)
        
        except Exception as e:
            logger.error(f"Error fetching dashboard data: {str(e)}")
            return Response(
                {'error': 'Unable to fetch dashboard data'},
                status=500
            )

class HomeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        available_attacks = [
            {"name": "Brute Force Attack", "description": "Test common credentials using brute force."},
            {"name": "SQL Injection", "description": "Test for SQL injection vulnerabilities."},
            {"name": "DoS Attack", "description": "Simulate denial-of-service conditions."},
            {"name": "XSS Attack", "description": "Check for Cross-Site Scripting vulnerabilities."},
            {"name": "Directory Traversal", "description": "Test for path traversal vulnerabilities."},
            {"name": "Command Injection", "description": "Attempt command injection exploits."},
            {"name": "CSRF Attack", "description": "Test for Cross-Site Request Forgery flaws."},
            {"name": "Vulnerability Scan", "description": "Scan for common vulnerabilities using heuristics."},
            {"name": "Port Scan", "description": "Identify open ports and services."},
            {"name": "Social Engineering Simulation", "description": "Simulate social engineering attack vectors."}
        ]
        return Response({"available_attacks": available_attacks})

class TermsView(APIView):
    def get(self, request):
        user_agreement = """
        User Agreement and Disclaimer

        1. Authorized Use Only: The services provided are for authorized, legal security testing of systems you own or have explicit permission to test.
        2. User Responsibility: You are solely responsible for compliance with all applicable laws. Any misuse or illegal activity is your responsibility.
        3. Prohibited Activities: Unauthorized penetration testing, malicious attacks, or any illegal use of these tools is strictly prohibited.
        4. Indemnification: You agree to hold harmless the website owners and developers from any claims arising from your misuse.
        5. Superuser/Administrator Protection: Administrative functions are secured via strong authentication.
        6. AI-Based Vulnerability Scanning: AI integrations are provided for research purposes only and should not be solely relied upon.
        """
        return Response({"user_agreement": user_agreement})
# dashboard/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from tests.models import Test
import logging

logger = logging.getLogger(__name__)

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        tests = Test.objects.filter(user=user).order_by('-start_time')
        running_count = Test.objects.filter(user=user, status__in=['Pending', 'Running']).count()

        dashboard_data = {
            'username': user.username,
            'profile_picture': user.profile_picture.url if user.profile_picture else None,
            'total_tests': tests.count(),
            'running_tests': running_count,
            'tests': [{
                'id': test.id,
                'test_name': test.test_name,
                'base_url': test.base_url,
                'status': test.status,
                'start_time': test.start_time,
                'end_time': test.end_time
            } for test in tests]
        }
        return Response(dashboard_data, status=200)
