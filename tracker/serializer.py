from rest_framework import serializers
from .models import CustomUser


class LoginSerilizer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=255)

    # password = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = ['email', 'password']


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validate_data):
        return CustomUser.objects.create_user(**validate_data)
