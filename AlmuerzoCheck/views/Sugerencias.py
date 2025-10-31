from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from AlmuerzoCheck.models import T005Sugerencias
from django.shortcuts import get_object_or_404
from AlmuerzoCheck.serializer.Sugerencias_Serializer import SugerenciaSerializer,SugerenciasAllSerializer


class CrearSugerenciaVista(generics.CreateAPIView):
    queryset = T005Sugerencias.objects.all()
    serializer_class = SugerenciaSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({
                'success': True,
                'detail': 'Sugerencia registrada correctamente',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            raise ValidationError(e.detail)
        except Exception as e:
            return Response({
                'success': False,
                'detail': 'Error al registrar la sugerencia',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







class EliminarSugerenciaVista(generics.DestroyAPIView):
    queryset = T005Sugerencias.objects.all()

    def delete(self, request, *args, **kwargs):
        try:
            sugerencia_id = kwargs.get('pk')  # Se espera que la URL sea /api/sugerencias/eliminar/<int:pk>/
            sugerencia = get_object_or_404(T005Sugerencias, pk=sugerencia_id)
            sugerencia.delete()

            return Response({
                'success': True,
                'detail': 'Sugerencia eliminada correctamente'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'success': False,
                'detail': 'Error al eliminar la sugerencia',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        






class ListarSugerenciasVista(generics.ListAPIView):
    queryset = T005Sugerencias.objects.select_related('estudiante', 'menu').all()
    serializer_class = SugerenciasAllSerializer

    def get(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()

            if not queryset.exists():
                return Response({
                    'success': True,
                    'detail': 'No hay sugerencias registradas',
                    'data': []
                }, status=status.HTTP_200_OK)

            serializer = self.get_serializer(queryset, many=True)
            return Response({
                'success': True,
                'detail': 'Lista de sugerencias registradas',
                'data': serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'success': False,
                'detail': 'Ocurrió un error al obtener las sugerencias',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)