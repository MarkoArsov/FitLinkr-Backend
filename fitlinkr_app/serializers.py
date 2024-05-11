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
        fields = ['id', 'user', 'name', 'description', 'price', 'category', 'location', 'rating']


class AppointmentSerializer(serializers.ModelSerializer):
    workout = serializers.PrimaryKeyRelatedField(queryset=Workout.objects.all())
    users = serializers.PrimaryKeyRelatedField(many=True, queryset=FitLinkrUser.objects.all(), required=False)
    class Meta:
        model = Appointment
        fields = ['id', 'workout', 'start_date', 'end_date', 'available_spots', 'users']
