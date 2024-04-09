from rest_framework import serializers
from .models import FitLinkrUser, Workout, Appointment

class FitLinkrUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = FitLinkrUser
        fields = ['id', 'username', 'password', 'phone_number']
        extra_kwargs = {'password': {'write_only': True}}

class WorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = ['id', 'user', 'name', 'description', 'price', 'category', 'location', 'available_spots', 'rating']

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'workout', 'start_date', 'end_date', 'available_spots', 'users']
