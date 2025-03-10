from rest_framework import serializers
from accounts.models import ShieldbotUser
from tests.models import Test

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    # Include the password field for write operations but make it write-only
    password = serializers.CharField(write_only=True)

    class Meta:
        model = ShieldbotUser
        fields = ['id', 'username', 'email', 'profile_picture', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = ShieldbotUser(**validated_data)
        user.set_password(password)  # Hash the password before saving
        user.save()
        return user
