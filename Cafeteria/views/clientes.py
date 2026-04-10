import json
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from ..models import Usuario, Cliente, Rol

# Función para generar códigos únicos
def generate_cod_usuario():
    last = Usuario.objects.order_by('-cod_usuario').first()
    if last:
        num = int(last.cod_usuario) + 1
        return f"{num:06d}"
    return "000001"

def generate_cod_cliente():
    last = Cliente.objects.order_by('-cod_cliente').first()
    if last:
        num = int(last.cod_cliente) + 1
        return f"{num:06d}"
    return "000001"

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def registrar_cliente(request):
    try:
        data = json.loads(request.body)
        nombre = data.get('nombre')
        correo = data.get('correo')
        password = data.get('password')
        telefono = data.get('telefono')
        direccion = data.get('direccion')

        if not all([nombre, correo, password, telefono, direccion]):
            return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            # Crear usuario
            cod_usuario = generate_cod_usuario()
            rol_cli = Rol.objects.get(cod_rol='CLI')
            usuario = Usuario.objects.create(
                cod_usuario=cod_usuario,
                nombre=nombre,
                correo=correo,
                password=password,  # En producción, hashear
                cod_rol=rol_cli
            )

            # Crear cliente
            cod_cliente = generate_cod_cliente()
            cliente = Cliente.objects.create(
                cod_cliente=cod_cliente,
                telefono=telefono,
                direccion=direccion,
                cod_usu=usuario
            )

        return Response({
            'message': 'Cliente registrado exitosamente',
            'cliente': {
                'cod_cliente': cliente.cod_cliente,
                'nombre': usuario.nombre,
                'correo': usuario.correo,
                'telefono': cliente.telefono,
                'direccion': cliente.direccion
            }
        }, status=status.HTTP_201_CREATED)

    except Rol.DoesNotExist:
        return Response({'error': 'Rol CLI no encontrado'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_clientes(request):
    clientes = Cliente.objects.select_related('cod_usu__cod_rol').all()
    data = []
    for cliente in clientes:
        data.append({
            'cod_cliente': cliente.cod_cliente,
            'nombre': cliente.cod_usu.nombre,
            'correo': cliente.cod_usu.correo,
            'telefono': cliente.telefono,
            'direccion': cliente.direccion,
            'rol': cliente.cod_usu.cod_rol.nombre
        })
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtener_cliente(request, cod_cliente):
    try:
        cliente = Cliente.objects.select_related('cod_usu__cod_rol').get(cod_cliente=cod_cliente)
        data = {
            'cod_cliente': cliente.cod_cliente,
            'nombre': cliente.cod_usu.nombre,
            'correo': cliente.cod_usu.correo,
            'telefono': cliente.telefono,
            'direccion': cliente.direccion,
            'rol': cliente.cod_usu.cod_rol.nombre
        }
        return Response(data)
    except Cliente.DoesNotExist:
        return Response({'error': 'Cliente no encontrado'}, status=status.HTTP_404_NOT_FOUND)

@csrf_exempt
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def actualizar_cliente(request, cod_cliente):
    try:
        cliente = Cliente.objects.select_related('cod_usu').get(cod_cliente=cod_cliente)
        data = json.loads(request.body)
        
        # Actualizar usuario
        if 'nombre' in data:
            cliente.cod_usu.nombre = data['nombre']
        if 'correo' in data:
            cliente.cod_usu.correo = data['correo']
        if 'password' in data:
            cliente.cod_usu.password = data['password']
        
        # Actualizar cliente
        if 'telefono' in data:
            cliente.telefono = data['telefono']
        if 'direccion' in data:
            cliente.direccion = data['direccion']
        
        cliente.cod_usu.save()
        cliente.save()
        
        return Response({'message': 'Cliente actualizado'})
    except Cliente.DoesNotExist:
        return Response({'error': 'Cliente no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def eliminar_cliente(request, cod_cliente):
    try:
        cliente = Cliente.objects.get(cod_cliente=cod_cliente)
        with transaction.atomic():
            usuario = cliente.cod_usu
            cliente.delete()
            usuario.delete()  # Eliminar usuario también
        return Response({'message': 'Cliente eliminado'})
    except Cliente.DoesNotExist:
        return Response({'error': 'Cliente no encontrado'}, status=status.HTTP_404_NOT_FOUND)