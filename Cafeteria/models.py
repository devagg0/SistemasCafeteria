from django.db import models

class Rol(models.Model):
    cod_rol = models.CharField(max_length=5, primary_key=True)
    nombre = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nombre

class Usuario(models.Model):
    cod_usuario = models.CharField(max_length=6, primary_key=True)
    nombre = models.CharField(max_length=50)
    correo = models.EmailField(unique=True)
    password = models.CharField(max_length=100)  # Note: In production, use hashed passwords
    cod_rol = models.ForeignKey(Rol, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    cod_cliente = models.CharField(max_length=6, primary_key=True)
    telefono = models.CharField(max_length=15, unique=True)
    direccion = models.CharField(max_length=100)
    cod_usu = models.OneToOneField(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.cod_usu.nombre} - {self.telefono}"
