from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from fitlinkr_app.serializers import FitLinkrUserSerializer
from fitlinkr_app.models import FitLinkrUser
from fitlinkr_app.models import Roles

class FitLinkrUserViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    # Payload:
    # {
    #     "username": "member_user",
    #     "password": "example_password",
    #     "role": "Member",
    #     "phone_number": "1234567890"
    # }
    # POST: /users/create_member/
    @action(detail=False, methods=['post'])
    def create_member(self, request):
        serializer = FitLinkrUserSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            phone_number = serializer.validated_data.get('phone_number')
            role = Roles.MEMBER
            user = FitLinkrUser.objects.create_user(username=username, password=password, phone_number=phone_number,
                                                    role=role)
            return Response({'message': 'Member created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Payload:
    # {
    #     "username": "trainer_user",
    #     "password": "example_password",
    #     "role": "Trainer",
    #     "phone_number": "1234567890"
    # }
    # POST: /users/create_trainer/
    @action(detail=False, methods=['post'])
    def create_trainer(self, request):
        serializer = FitLinkrUserSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            phone_number = serializer.validated_data.get('phone_number')
            role = Roles.TRAINER
            user = FitLinkrUser.objects.create_user(username=username, password=password, phone_number=phone_number,
                                                    role=role)
            return Response({'message': 'Trainer created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Payload:
    # {
    #     "username": "updated_username",
    #     "password": "updated_password",
    #     "phone_number": "updated_phone_number"
    # }
    # POST: /users/<user_id>/
    def update(self, request, pk=None):
        try:
            user = FitLinkrUser.objects.get(pk=pk)
            serializer = FitLinkrUserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except FitLinkrUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    # Payload:
    # {
    #     "username": "example_user",
    #     "password": "example_password"
    # }
    # POST: /users/login/
    @action(detail=False, methods=['post'])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return Response({'message': 'Login successful'})
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    # POST: /users/logout/
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        logout(request)
        return Response({'message': 'Logout successful'})

    # GET: /users/current_user/
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def current_user(self, request):
        serializer = FitLinkrUserSerializer(request.user)
        return Response(serializer.data)

    # GET: /users/list_users/
    @action(detail=False, methods=['get'])
    def list_users(self, request):
        queryset = FitLinkrUser.objects.all()
        serializer = FitLinkrUserSerializer(queryset, many=True)
        return Response(serializer.data)

    # GET: /users/<user_id>/read/
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def read(self, request, pk=None):
        try:
            user = FitLinkrUser.objects.get(pk=pk)
            serializer = FitLinkrUserSerializer(user)
            return Response(serializer.data)
        except FitLinkrUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    # DELETE: /users/<user_id>/delete/
    @action(detail=True, methods=['delete'], permission_classes=[IsAuthenticated])
    def delete(self, request, pk=None):
        try:
            user = FitLinkrUser.objects.get(pk=pk)
            user.delete()
            return Response({'message': 'User deleted successfully'})
        except FitLinkrUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
