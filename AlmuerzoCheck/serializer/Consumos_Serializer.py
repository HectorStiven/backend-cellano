from rest_framework import serializers
from AlmuerzoCheck.models import T001Estudiantes, T004Consumos




class ConsumosSerializer(serializers.ModelSerializer):
    class Meta:
        model = T004Consumos
        fields = "__all__"


class ConsumoSerializer(serializers.ModelSerializer):
    plato_principal = serializers.CharField(source='menu.plato_principal', read_only=True)
    identificacion = serializers.CharField(source='estudiante.identificacion', read_only=True)
    fotoId = serializers.ImageField(source='estudiante.fotoId', read_only=True)
    primer_nombre = serializers.CharField(source='estudiante.primer_nombre', read_only=True)
    creditos = serializers.DecimalField(source='estudiante.creditos', max_digits=10, decimal_places=2, read_only=True)
    grado = serializers.CharField(source='estudiante.grado', read_only=True)
    class Meta:
        model = T004Consumos
        fields = [
            'id',
            'estudiante',
            'menu',
            'plato_principal',  # 👈 nombre del plato del menú
            'fecha',
            'hora',
            'identificacion',  # 👈 identificación del estudiante
            'fotoId',
            'primer_nombre',
            'creditos',
            'grado',
        ]



class EstudianteSinConsumoSerializer(serializers.ModelSerializer):
    fotoId = serializers.ImageField(use_url=True)  # Devuelve la URL automáticamente

    class Meta:
        model = T001Estudiantes
        fields = ['id', 'identificacion', 'primer_nombre', 'fotoId', 'creditos', 'grado']
