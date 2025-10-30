from AlmuerzoCheck.models import T001Estudiantes
from rest_framework import serializers

class EstudianteSerializer(serializers.ModelSerializer):
    class Meta:
        model = T001Estudiantes
        fields = '__all__'


class EstudianteAllSerializer(serializers.ModelSerializer):
    """
    Serializer para mostrar información básica del estudiante.
    """
    class Meta:
        model = T001Estudiantes
        fields = [
            'id',
            'identificacion',
            'primer_nombre',
            'segundo_nombre',
            'primer_apellido',
            'segundo_apellido',
            'grado',
            'fotoId',
            'genero'
        ]