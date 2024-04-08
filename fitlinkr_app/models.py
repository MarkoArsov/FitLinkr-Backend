from django.db import models
from django.contrib.auth.models import AbstractUser

class Roles(models.TextChoices):
        MEMBER = 'member', 'Member'
        TRAINER = 'trainer', 'Trainer'
class FitLinkrUser(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(max_length=10, choices=Roles.choices, default=Roles.MEMBER)