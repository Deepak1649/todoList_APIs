from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login, authenticate
from rest_framework.permissions import IsAuthenticated
from todolist_app.serializers import TodoTaskSerializer
from .models import TodoTask
from .serializers import TodoTaskSerializer
from rest_framework.decorators import api_view, permission_classes


@api_view(['POST'])
def user_register(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        if not username or not password or not email:
            return Response({'error': 'Please provide username, password, and email.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.create_user(username=username, password=password, email=email)
        except Exception as e:
            return Response({'error': 'User registration failed.'}, status=status.HTTP_400_BAD_REQUEST)

        login(request, user)
        return Response({'message': 'User registered successfully.'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def user_login(request):
     if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return Response({'message': 'Login successful.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Login failed. Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_todo_task(request):
    
    request.data['user'] = request.user.id
    serializer = TodoTaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_todo_task(request, task_id):
    try:
        task = get_object_or_404(TodoTask, id=task_id)
        if task.user != request.user:
            return Response({'error': 'You do not have permission to update this task.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = TodoTaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except TodoTask.DoesNotExist:
        return Response({'error': 'Task not found.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_todo_task(request, task_id):
    try:
        task = get_object_or_404(TodoTask, id=task_id)
        if task.user != request.user:
            return Response({'error': 'You do not have permission to delete this task.'}, status=status.HTTP_403_FORBIDDEN)

        task.delete()
        return Response({'message': 'Task deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    except TodoTask.DoesNotExist:
        return Response({'error': 'Task not found.'}, status=status.HTTP_404_NOT_FOUND)