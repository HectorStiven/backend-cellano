from AlmuerzoCheck.models import T008Acudientes
from rest_framework import serializers

class AcudienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = T008Acudientes
        fields = '__all__'