from django.db import models
from django.contrib.auth.models import AbstractUser

class Roles(models.TextChoices):
    MEMBER = 'member', 'Member'
    TRAINER = 'trainer', 'Trainer'
class FitLinkrUser(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(max_length=10, choices=Roles.choices, default=Roles.MEMBER)


class Categories(models.TextChoices):
    STRENGTH = 'strength', 'Strength Training'
    CARDIO = 'cardio', 'Cardio'
    YOGA = 'yoga', 'Yoga'
    PILATES = 'pilates', 'Pilates'
    CROSSFIT = 'crossfit', 'CrossFit'
    OTHER = 'other', 'Other'

class Workout(models.Model):
    user = models.ForeignKey(FitLinkrUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=10, choices=Categories.choices, default=Categories.OTHER)
    location = models.CharField(max_length=100)
    available_spots = models.PositiveIntegerField()
    rating = models.FloatField()


class Appointment(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    available_spots = models.PositiveIntegerField()
    users = models.ManyToManyField(FitLinkrUser)
