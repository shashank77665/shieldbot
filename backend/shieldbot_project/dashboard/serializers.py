from rest_framework import serializers
from tests.models import Test

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ['id', 'test_name', 'base_url', 'status', 'start_time', 'end_time']