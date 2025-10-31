from rest_framework import serializers
from AlmuerzoCheck.models import T004Consumos




class ConsumosSerializer(serializers.ModelSerializer):
    class Meta:
        model = T004Consumos
        fields = "__all__"


class ConsumoSerializer(serializers.ModelSerializer):
    plato_principal = serializers.CharField(source='menu.plato_principal', read_only=True)

    class Meta:
        model = T004Consumos
        fields = [
            'id',
            'estudiante',
            'menu',
            'plato_principal',  # 👈 nombre del plato del menú
            'fecha',
            'hora',
        ]