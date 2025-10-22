from AlmuerzoCheck.models import T001Estudiantes
from rest_framework import serializers

class EstudianteSerializer(serializers.ModelSerializer):
    class Meta:
        model = T001Estudiantes
        fields = '__all__'