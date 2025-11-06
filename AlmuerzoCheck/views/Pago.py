from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from datetime import date
import calendar  # 📅 Para saber cuántos días tiene el mes

from AlmuerzoCheck.models import T002Pagos, T001Estudiantes
from AlmuerzoCheck.serializer.Pago_Serializer import PagoSerializer, PagoDetalleSerializer




class CrearPagoVista(generics.CreateAPIView):
    queryset = T002Pagos.objects.all()
    serializer_class = PagoSerializer

    def create(self, request, *args, **kwargs):
        try:
            estudiante_id = request.data.get("estudiante")
            mes = request.data.get("mes")
            anio = request.data.get("anio")
            valor_mensualidad = request.data.get("valor_mensualidad")

            # 🧩 Validación: se requiere ID del estudiante
            if not estudiante_id:
                return Response({
                    'success': False,
                    'detail': 'Debe indicar el ID del estudiante.'
                }, status=status.HTTP_400_BAD_REQUEST)

            # 🔍 Verificar que el estudiante existe
            estudiante = T001Estudiantes.objects.filter(id=estudiante_id).first()
            if not estudiante:
                return Response({
                    'success': False,
                    'detail': f'No existe estudiante con ID {estudiante_id}.'
                }, status=status.HTTP_404_NOT_FOUND)

            # 🚫 Evitar pagos duplicados del mismo mes y año
            if T002Pagos.objects.filter(estudiante=estudiante, mes=mes, anio=anio).exists():
                return Response({
                    'success': False,
                    'detail': 'Ya existe un pago registrado para este mes y año.'
                }, status=status.HTTP_400_BAD_REQUEST)

            # 🧮 Calcular los días del mes (créditos)
            dias_en_mes = calendar.monthrange(int(anio), int(mes))[1]  # Ej: febrero = 28

            # ✅ Crear el pago
            pago = T002Pagos.objects.create(
                estudiante=estudiante,
                mes=mes,
                anio=anio,
                valor_mensualidad=valor_mensualidad,
                fecha_pago=date.today()
            )

            # 🔁 Actualizar estado y créditos del estudiante
            estudiante.estado = True
            estudiante.creditos += dias_en_mes
            estudiante.save()

            # 📦 Serializar pago creado
            serializer = self.get_serializer(pago)
            return Response({
                'success': True,
                'detail': f'Pago confirmado para {estudiante.primer_nombre} {estudiante.primer_apellido}. '
                          f'Se añadieron {dias_en_mes} créditos.',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            raise ValidationError(e.detail)
        except Exception as e:
            return Response({
                'success': False,
                'detail': 'Error al registrar el pago',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





class ListarPagosPorMesAnioVista(generics.ListAPIView):
    serializer_class = PagoDetalleSerializer

    def get_queryset(self):
        # 🔍 Obtener parámetros de la URL o querystring
        mes = self.request.query_params.get('mes')
        anio = self.request.query_params.get('anio')

        # Validar que los parámetros existan
        if not mes or not anio:
            return T002Pagos.objects.none()

        # Filtrar por mes y año
        return T002Pagos.objects.filter(mes=mes, anio=anio).select_related('estudiante')

    def list(self, request, *args, **kwargs):
        mes = request.query_params.get('mes')
        anio = request.query_params.get('anio')

        if not mes or not anio:
            return Response({
                'success': False,
                'detail': 'Debe indicar mes y año. Ejemplo: ?mes=10&anio=2025'
            }, status=status.HTTP_400_BAD_REQUEST)

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success': True,
            'detail': f'Pagos del mes {mes} del año {anio}',
            'cantidad': queryset.count(),
            'data': serializer.data
        }, status=status.HTTP_200_OK)