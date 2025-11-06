from AlmuerzoCheck.models import T001Estudiantes
from rest_framework import serializers

class EstudianteSerializer(serializers.ModelSerializer):
    fotoId = serializers.ImageField(use_url=True)  # Devuelve la URL automáticamente
    class Meta:
        model = T001Estudiantes
        fields = '__all__'


class EstudianteAllSerializer(serializers.ModelSerializer):
    """    fotoId = serializers.ImageField(use_url=True)  # Devuelve la URL automáticamente
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
            'genero',
            'estado',
            'creditos'
        ]