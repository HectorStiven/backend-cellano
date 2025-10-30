from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from AlmuerzoCheck.models import T001Estudiantes
from AlmuerzoCheck.serializer.Estudiantes_Serializer import EstudianteSerializer
from rest_framework.permissions import IsAuthenticated  
from rest_framework.parsers import MultiPartParser, FormParser


class CrearEstudianteVista(generics.CreateAPIView):
    queryset = T001Estudiantes.objects.all()
    serializer_class = EstudianteSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]  # Permite subir archivos

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response({
                "success": True,
                "detail": "Estudiante registrado correctamente",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({
                "success": False,
                "detail": "Error de validación al registrar al estudiante",
                "errors": e.detail
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "success": False,
                "detail": "Ocurrió un error interno del servidor",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ListarEstudiantesVista(generics.ListAPIView):
    """
    Vista para listar todos los estudiantes.
    Acepta peticiones GET.
    """
    queryset = T001Estudiantes.objects.all()  # Trae todos los estudiantes
    serializer_class = EstudianteSerializer
    permission_classes = [IsAuthenticated]  

    def get(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            
            if not queryset.exists():
                return Response({
                    "success": True,
                    "detail": "No se encontraron estudiantes",
                    "data": []
                }, status=status.HTTP_200_OK)

            serializer = self.get_serializer(queryset, many=True)
            
            return Response({
                "success": True,
                "detail": f"Lista de {queryset.count()} estudiantes",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                "success": False,
                "detail": "Ocurrió un error al obtener la lista de estudiantes",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
