from rest_framework import serializers
from .models import FitLinkrUser

class FitLinkrUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = FitLinkrUser
        fields = ['id', 'username', 'password', 'phone_number'] 
        extra_kwargs = {'password': {'write_only': True}} 