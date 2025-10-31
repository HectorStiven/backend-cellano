from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from django.shortcuts import get_object_or_404

from AlmuerzoCheck.models import T004Consumos
from AlmuerzoCheck.serializer.Consumos_Serializer import ConsumosSerializer,ConsumoSerializer


class CrearConsumoVista(generics.CreateAPIView):
    queryset = T004Consumos.objects.all()
    serializer_class = ConsumosSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({
                'success': True,
                'detail': 'Consumo registrado correctamente',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            raise ValidationError(e.detail)
        except Exception as e:
            return Response({
                'success': False,
                'detail': 'Error al registrar el consumo',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        






class ListarConsumosPorEstudianteVista(generics.ListAPIView):
    serializer_class = ConsumoSerializer

    def get_queryset(self):
        estudiante_id = self.kwargs.get('estudiante_id')
        return T004Consumos.objects.filter(estudiante_id=estudiante_id)

    def get(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()

            if not queryset.exists():
                return Response({
                    'success': True,
                    'detail': 'No hay consumos registrados para este estudiante',
                    'data': []
                }, status=status.HTTP_200_OK)

            serializer = self.get_serializer(queryset, many=True)
            return Response({
                'success': True,
                'detail': 'Lista de consumos del estudiante',
                'data': serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'success': False,
                'detail': 'Ocurrió un error al obtener los consumos',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)