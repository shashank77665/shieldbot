# attacks/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class PerformTestView(APIView):
    def post(self, request, *args, **kwargs):
        # Implement your logic to perform the test here.
        data = {"message": "PerformTestView: Attack test initiated."}
        return Response(data, status=status.HTTP_200_OK)

class TestStatusView(APIView):
    def get(self, request, test_id, *args, **kwargs):
        # Logic to retrieve test status based on test_id.
        data = {"message": f"TestStatusView: Status for test id {test_id}."}
        return Response(data, status=status.HTTP_200_OK)

class ListTestsView(APIView):
    def get(self, request, *args, **kwargs):
        # Logic to list all tests.
        data = {"message": "ListTestsView: Listing tests."}
        return Response(data, status=status.HTTP_200_OK)

class StartAttackView(APIView):
    def post(self, request, *args, **kwargs):
        # Logic to start an attack.
        data = {"message": "StartAttackView: Attack started."}
        return Response(data, status=status.HTTP_200_OK)

class StopDDoSView(APIView):
    def post(self, request, *args, **kwargs):
        # Logic to stop a DDoS attack.
        data = {"message": "StopDDoSView: DDoS attack stopped."}
        return Response(data, status=status.HTTP_200_OK)

class StopAllDDoSView(APIView):
    def post(self, request, *args, **kwargs):
        # Logic to stop all DDoS attacks.
        data = {"message": "StopAllDDoSView: All DDoS attacks stopped."}
        return Response(data, status=status.HTTP_200_OK)

class GetCommandView(APIView):
    def get(self, request, *args, **kwargs):
        # Logic to return a command for attack agents.
        data = {"execute": False, "message": "GetCommandView: No command to execute."}
        return Response(data, status=status.HTTP_200_OK)

class ExecuteAttackView(APIView):
    def post(self, request, *args, **kwargs):
        # Logic to execute an attack command.
        data = {"message": "ExecuteAttackView: Attack command executed."}
        return Response(data, status=status.HTTP_200_OK)
# attacks/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from tests.models import Test
from . import ddos_attack, brute_force, port_scan, custom_api  # Ensure these modules expose a callable function

class StartAttackView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        base_url = request.data.get('base_url')
        attack_type = request.data.get('attack_type', '').lower()
        options = request.data.get('options', {})

        if not base_url or not attack_type:
            return Response(
                {"error": "Both 'base_url' and 'attack_type' are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create a test record with status "Pending"
        test = Test.objects.create(
            user=user,
            base_url=base_url,
            test_type=attack_type,
            status="Pending",
            start_time=timezone.now()
        )

        # Dispatch to the correct test function based on attack_type
        if attack_type == "ddos":
            result = ddos_attack.ddos_attack_test(base_url, options)
        elif attack_type == "brute_force":
            result = brute_force.brute_force_test(base_url, options)
        elif attack_type == "port_scan":
            result = port_scan.port_scan_test(base_url, options)
        elif attack_type == "api":
            result = custom_api.custom_api_test(base_url, options)
        else:
            return Response(
                {"error": f"Invalid attack_type '{attack_type}'. Valid options: ddos, brute_force, port_scan, api."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Update test record with results
        test.logs = result
        test.status = "Completed"
        test.end_time = timezone.now()
        test.save()

        return Response({
            "message": f"{attack_type.capitalize()} test performed successfully.",
            "test_id": test.id,
            "results": result
        }, status=status.HTTP_200_OK)
