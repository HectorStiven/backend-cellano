# En tu_app/views.py

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from AlmuerzoCheck.models import T001Estudiantes # Asegúrate de que esta importación sea correcta
from AlmuerzoCheck.serializer.Estudiantes_Serializer import EstudianteSerializer # Importa tu nuevo serializador
from rest_framework.permissions import IsAuthenticated  



class CrearEstudianteVista(generics.CreateAPIView):

    queryset = T001Estudiantes.objects.all()
    serializer_class = EstudianteSerializer
    permission_classes = [IsAuthenticated]  # Asegúrate de que se requiera autenticación

    def create(self, request, *args, **kwargs):
        try:
            # 1. Obtiene el serializador y pasa los datos de la solicitud
            serializer = self.get_serializer(data=request.data)
            
            # 2. Valida los datos. Si fallan, lanza una excepción ValidationError
            serializer.is_valid(raise_exception=True)
            
            # 3. Guarda el nuevo objeto en la base de datos
            self.perform_create(serializer) # Llama a serializer.save()
            
            # 4. Retorna la respuesta HTTP 201 Created (creado con éxito)
            return Response({
                'success': True,
                'detail': 'Estudiante registrado correctamente',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
            
        except ValidationError as e:
            # Captura errores de validación (ej. identificación duplicada)
            return Response({
                'success': False,
                'detail': 'Error de validación al registrar al estudiante',
                'errors': e.detail # Aquí estarán los detalles del error (ej. {'identificacion': ['Ya existe T001_identificación.']})
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # Captura cualquier otro error inesperado
            return Response({
                'success': False,
                'detail': 'Ocurrió un error interno del servidor',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class ListarEstudiantesVista(generics.ListAPIView):
    """
    Vista para listar todos los estudiantes.
    Acepta peticiones GET.
    """
    # Define todos los objetos que pueden ser listados (Estudiantes activos)
    queryset = T001Estudiantes.objects.filter(estado=True)
    serializer_class = EstudianteSerializer


    def get(self, request, *args, **kwargs):
        try:
            # Obtiene y filtra el queryset (en este caso, solo activos)
            queryset = self.filter_queryset(self.get_queryset())
            
            # Verifica si hay registros
            if not queryset.exists():
                return Response({
                    'success': True,
                    'detail': 'No se encontraron estudiantes activos.',
                    'data': []
                }, status=status.HTTP_200_OK)

            # Serializa la lista de objetos
            serializer = self.get_serializer(queryset, many=True)
            
            # Retorna la respuesta con la lista de datos
            return Response({
                'success': True,
                'detail': f'Lista de {queryset.count()} estudiantes activos.',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'success': False,
                'detail': 'Ocurrió un error al obtener la lista de estudiantes',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)