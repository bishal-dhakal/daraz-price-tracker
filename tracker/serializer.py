from rest_framework import serializers
from django.contrib.auth.models import User

class LoginSerilizer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255)
    # password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username','password']
        
    

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','password']
        extra_kwargs= {
            'password':{'write_only':True}
        }
    
    def create(self, validate_data):
        return User.objects.create_user(**validate_data)
