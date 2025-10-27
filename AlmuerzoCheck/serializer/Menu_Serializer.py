from rest_framework import serializers
from AlmuerzoCheck.models import T003MenuDia

# Serializer para el modelo T008Menu
class MenuSerializer(serializers.ModelSerializer):  
    class Meta:
        model = T003MenuDia
        fields = "__all__"  # Incluye todos los campos del modelo



