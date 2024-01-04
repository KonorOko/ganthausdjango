from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User
from rest_framework import serializers


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # Add your extra responses here
        data['username'] = self.user.username
        data['groups'] = self.user.groups.values_list('name', flat=True)
        return data

class UserSerializer(serializers.ModelSerializer):
    username = serializers.StringRelatedField()
    group = serializers.StringRelatedField()
    
    class Meta:
        model = User
        exclude = ['password', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'groups', 'user_permissions', 'last_login']