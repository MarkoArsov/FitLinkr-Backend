from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets
from fitlinkr_app.models import Appointment, Workout
from fitlinkr_app.serializers import AppointmentSerializer

class AppointmentViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    # Payload:
    # {
    #     "workout": 1,
    #     "start_date": "2022-03-01T10:00:00Z",
    #     "end_date": "2022-03-01T11:00:00Z",
    #     "available_spots": 10
    # }
    # POST: /appointments/create_appointment/
    @action(detail=False, methods=['post'])
    def create_appointment(self, request):
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            workout_id = serializer.validated_data['workout'].id
            start_date = serializer.validated_data['start_date']
            end_date = serializer.validated_data['end_date']
            available_spots = serializer.validated_data['available_spots']
            users = serializer.validated_data.get('users', [])

            try:
                workout = Workout.objects.get(pk=workout_id)
            except Workout.DoesNotExist:
                return Response({'error': 'Workout not found'}, status=status.HTTP_404_NOT_FOUND)

            appointment = Appointment.objects.create(
                workout=workout,
                start_date=start_date,
                end_date=end_date,
                available_spots=available_spots,
            )

            return Response({'message': 'Appointment created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    # Payload:
    # {
    #     "workout": 1,
    #     "start_date": "2022-03-01T10:00:00Z",
    #     "end_date": "2022-03-01T11:00:00Z",
    #     "available_spots": 10
    # }
    # PUT: /appointments/<appointment_id>/update/
    @action(detail=True, methods=['put'], permission_classes=[IsAuthenticated])
    def update_appointment(self, request, pk=None):
        try:
            appointment = Appointment.objects.get(pk=pk)
            serializer = AppointmentSerializer(appointment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Appointment.DoesNotExist:
            return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # DELETE: /appointments/<appointment_id>/delete/
    @action(detail=True, methods=['delete'], permission_classes=[IsAuthenticated])
    def delete_appointment(self, request, pk=None):
        try:
            appointment = Appointment.objects.get(pk=pk)
            appointment.delete()
            return Response({'message': 'Appointment deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Appointment.DoesNotExist:
            return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # GET: /appointments/<appointment_id>/read/
    @action(detail=True, methods=['get'])
    def read(self, request, pk=None):
        try:
            appointment = Appointment.objects.get(pk=pk)
            serializer = AppointmentSerializer(appointment)
            return Response(serializer.data)
        except Appointment.DoesNotExist:
            return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)

    # GET: /appointments/list_appointments/
    @action(detail=False, methods=['get'])
    def list_appointments(self, request):
        queryset = Appointment.objects.all()
        serializer = AppointmentSerializer(queryset, many=True)
        return Response(serializer.data)

    # GET: /appointments/list_appointments_by_workout/<workout_id>/
    @action(detail=False, methods=['get'])
    def list_appointments_by_workout(self, request, workout_id=None):
        try:
            appointments = Appointment.objects.filter(workout_id=workout_id)
            serializer = AppointmentSerializer(appointments, many=True)
            return Response(serializer.data)
        except Workout.DoesNotExist:
            return Response({'error': 'Workout not found'}, status=status.HTTP_404_NOT_FOUND)

    # GET: /appointments/list_appointments_by_user/<user_id>/
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def list_appointments_by_user(self, request, user_id=None):
        try:
            appointments = Appointment.objects.filter(users__id=user_id)
            serializer = AppointmentSerializer(appointments, many=True)
            return Response(serializer.data)
        except Appointment.DoesNotExist:
            return Response({'error': 'User has no appointments'}, status=status.HTTP_404_NOT_FOUND)
    
    # POST: /appointments/<appointment_id>/make_reservation/
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def make_reservation(self, request, pk=None):
        try:
            appointment = Appointment.objects.get(pk=pk)

            # Check if there are available spots
            if appointment.available_spots > 0:
                # Add the authenticated user to the appointment
                appointment.users.add(request.user)
                appointment.available_spots -= 1
                appointment.save()

                return Response({'message': 'Reservation made successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'No available spots for this appointment'}, status=status.HTTP_400_BAD_REQUEST)

        except Appointment.DoesNotExist:
            return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)

    # DELETE: /appointments/<appointment_id>/cancel_reservation/
    @action(detail=True, methods=['delete'], permission_classes=[IsAuthenticated])
    def cancel_reservation(self, request, pk=None):
        try:
            appointment = Appointment.objects.get(pk=pk)

            # Check if the user has a reservation for this appointment
            if request.user in appointment.users.all():
                # Remove the user from the appointment
                appointment.users.remove(request.user)
                appointment.available_spots += 1
                appointment.save()

                return Response({'message': 'Reservation canceled successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'User does not have a reservation for this appointment'}, status=status.HTTP_400_BAD_REQUEST)

        except Appointment.DoesNotExist:
            return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)
        
