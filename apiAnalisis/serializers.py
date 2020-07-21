from rest_framework import serializers
from apiAnalisis import models

class LibroSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'titulo',
            'descripcion',
        )
        model = models.Libro

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'cedula',
            'edad',
            'tipoCliente',
        )
        model = models.Cliente

class GraficaSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'imagen',
            'titulo',
        )
        model = models.Grafica