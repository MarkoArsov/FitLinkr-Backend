from rest_framework import viewsets
from rest_framework.permissions import AllowAny

class WorkoutViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]