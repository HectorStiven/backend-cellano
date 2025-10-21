from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from AlmuerzoCheck.models import T008Acudientes
from AlmuerzoCheck.serializer.Acudiente_Serializer import AcudienteSerializer
from AlmuerzoCheck.models import T001Estudiantes
from django.shortcuts import get_object_or_404

# Crear Acudiente
class CrearAcudienteVista(generics.CreateAPIView):
    queryset = T008Acudientes.objects.all()
    serializer_class = AcudienteSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({
                'success': True,
                'detail': 'Acudiente registrado correctamente',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            raise ValidationError(e.detail)




class ListarAcudientesVista(generics.ListAPIView):
    serializer_class = AcudienteSerializer

    def get_queryset(self):
        estudiante_id = self.kwargs.get('estudiante_id')
        # Verifica que el estudiante exista
        estudiante = get_object_or_404(T001Estudiantes, id=estudiante_id)
        # Retorna los acudientes del estudiante
        return T008Acudientes.objects.filter(estudiante=estudiante)

    def get(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            if not queryset.exists():
                return Response({
                    'success': True,
                    'detail': 'No hay acudientes para este estudiante',
                    'data': []
                }, status=status.HTTP_200_OK)

            serializer = self.get_serializer(queryset, many=True)
            return Response({
                'success': True,
                'detail': 'Lista de acudientes del estudiante',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({
                'success': False,
                'detail': 'Ocurrió un error al obtener los acudientes',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


# Actualizar Acudiente
class ActualizarAcudienteVista(generics.UpdateAPIView):
    queryset = T008Acudientes.objects.all()
    serializer_class = AcudienteSerializer

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=kwargs.get('partial', False))
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'success': True,
            'detail': 'Acudiente actualizado correctamente',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

# Borrar Acudiente
class BorrarAcudienteVista(generics.DestroyAPIView):
    queryset = T008Acudientes.objects.all()
    serializer_class = AcudienteSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'success': True,
            'detail': 'Acudiente eliminado correctamente'
        }, status=status.HTTP_200_OK)
