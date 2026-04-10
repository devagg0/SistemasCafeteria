import json
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from ..models import Usuario

@csrf_exempt
@api_view(['POST'])
def login_view(request):
    try:
        data = json.loads(request.body)
        correo = data.get('username')
        password = data.get('password')
        user = Usuario.objects.get(correo=correo, password=password)
        refresh = RefreshToken()
        refresh['user_id'] = user.cod_usuario
        refresh['user_name'] = user.nombre
        refresh['user_role'] = user.cod_rol.nombre
        access = refresh.access_token
        access['user_id'] = user.cod_usuario
        access['user_name'] = user.nombre
        access['user_role'] = user.cod_rol.nombre
        return Response({
            'refresh': str(refresh),
            'access': str(access),
            'user': {'name': user.nombre, 'role': user.cod_rol.nombre}
        })
    except Usuario.DoesNotExist:
        return Response({'error': 'Invalid credentials'}, status=400)
    except json.JSONDecodeError:
        return Response({'error': 'Invalid JSON'}, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def home_view(request):
    token = request.auth
    if token:
        user_data = {
            'user_id': token.get('user_id'),
            'name': token.get('user_name'),
            'role': token.get('user_role')
        }
    else:
        user_data = None
    return Response({
        'message': 'Welcome to the API',
        'user': user_data
    })

@csrf_exempt
@api_view(['POST'])
def logout_view(request):
    return Response({'message': 'Logged out successfully'})