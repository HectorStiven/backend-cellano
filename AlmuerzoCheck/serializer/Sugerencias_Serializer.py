from AlmuerzoCheck.models import T005Sugerencias
from rest_framework import serializers
from AlmuerzoCheck.serializer.Estudiantes_Serializer import EstudianteSerializer
class SugerenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = T005Sugerencias
        fields = '__all__'



class SugerenciasAllSerializer(serializers.ModelSerializer):
    estudiante = EstudianteSerializer(read_only=True)

    class Meta:
        model = T005Sugerencias
        fields = '__all__'