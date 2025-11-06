from AlmuerzoCheck.models import T002Pagos
from rest_framework import serializers

class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = T002Pagos
        fields = '__all__'





class PagoDetalleSerializer(serializers.ModelSerializer):
    # 🔗 Campos del estudiante concatenados
    estudiante_nombre_completo = serializers.SerializerMethodField()
    identificacion = serializers.CharField(source='estudiante.identificacion', read_only=True)
    grado = serializers.CharField(source='estudiante.grado', read_only=True)
    grupo = serializers.CharField(source='estudiante.grupo', read_only=True)
    jornada = serializers.CharField(source='estudiante.jornada', read_only=True)

    class Meta:
        model = T002Pagos
        fields = [
            'id',
            'mes',
            'anio',
            'valor_mensualidad',
            'fecha_pago',
            'identificacion',
            'estudiante_nombre_completo',
            'grado',
            'grupo',
            'jornada',
        ]

    def get_estudiante_nombre_completo(self, obj):
        estudiante = obj.estudiante
        return f"{estudiante.primer_nombre} {estudiante.segundo_nombre or ''} {estudiante.primer_apellido} {estudiante.segundo_apellido or ''}".strip()