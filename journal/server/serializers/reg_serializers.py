from rest_framework import serializers
from server.models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'middle_name', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user