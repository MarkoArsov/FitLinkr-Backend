from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import viewsets
from fitlinkr_app.models import Workout
from fitlinkr_app.models import Categories
from fitlinkr_app.serializers import WorkoutSerializer
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

@method_decorator(csrf_exempt, name='dispatch')
class WorkoutViewSet(viewsets.ViewSet):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    # POST: /workouts/create_workout/
    @action(detail=False, methods=['post'])
    def create_workout(self, request):
        serializer = WorkoutSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Workout created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # POST: /workouts/<workout_id>/
    def update(self, request, pk=None):
        try:
            workout = Workout.objects.get(pk=pk)
            serializer = WorkoutSerializer(workout, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Workout updated successfully'})
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Workout.DoesNotExist:
            return Response({'error': 'Workout not found'}, status=status.HTTP_404_NOT_FOUND)

    # DELETE: /workouts/<workout_id>/delete/
    @action(detail=True, methods=['delete'])
    def delete(self, request, pk=None):
        try:
            workout = Workout.objects.get(pk=pk)
            workout.delete()
            return Response({'message': 'Workout deleted successfully'})
        except Workout.DoesNotExist:
            return Response({'error': 'Workout not found'}, status=status.HTTP_404_NOT_FOUND)

    # GET: /workouts/list_workouts/
    @action(detail=False, methods=['get'])
    def list_workouts(self, request):
        category_param = request.query_params.get('category', None)
        
        if category_param:
            queryset = Workout.objects.filter(category=category_param)
        else:
            queryset = Workout.objects.all()
        
        serializer = WorkoutSerializer(queryset, many=True)
        return Response(serializer.data)

    # GET: /workouts/list_categories/
    @action(detail=False, methods=['get'])
    def list_categories(self, request):
        categories = [category.value for category in Categories]
        return Response(categories)
    
    # GET: /workouts/list_workouts_by_user/
    @action(detail=False, methods=['get'])
    def list_workouts_by_user(self, request):
        user = request.user
        queryset = Workout.objects.filter(user=user)
        serializer = WorkoutSerializer(queryset, many=True)
        return Response(serializer.data)
    
    # GET: /workouts/<workout_id>/read/
    @action(detail=True, methods=['get'])
    def read(self, request, pk=None):
        try:
            workout = Workout.objects.get(pk=pk)
            serializer = WorkoutSerializer(workout)
            return Response(serializer.data)
        except Workout.DoesNotExist:
            return Response({'error': 'Workout not found'}, status=status.HTTP_404_NOT_FOUND)