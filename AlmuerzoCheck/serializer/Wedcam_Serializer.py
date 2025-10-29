from rest_framework import serializers
from AlmuerzoCheck.models import T001Estudiantes

class EstudianteSerializer(serializers.ModelSerializer):
    class Meta:
        model = T001Estudiantes
        fields = '__all__'
