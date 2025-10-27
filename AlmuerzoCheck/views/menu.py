from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from AlmuerzoCheck.models import T003MenuDia
from AlmuerzoCheck.serializer.Menu_Serializer import MenuSerializer



class CrearMenuVista(generics.CreateAPIView):
    """
    Vista para crear un nuevo menú del día.
    """
    queryset = T003MenuDia.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            # 1. Obtiene el serializador con los datos enviados
            serializer = self.get_serializer(data=request.data)
            
            # 2. Valida los datos
            serializer.is_valid(raise_exception=True)
            
            # 3. Guarda el menú en la base de datos
            self.perform_create(serializer)
            
            # 4. Respuesta exitosa
            return Response({
                'success': True,
                'detail': 'Menú creado correctamente',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            # Captura errores de validación
            return Response({
                'success': False,
                'detail': 'Error de validación al crear el menú',
                'errors': e.detail
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # Captura errores inesperados
            return Response({
                'success': False,
                'detail': 'Ocurrió un error interno al crear el menú',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





class ListarMenuVista(generics.ListAPIView):
    """
    Vista para listar todos los menús del día.
    """
    queryset = T003MenuDia.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset().order_by('fecha'))

            if not queryset.exists():
                return Response({
                    'success': True,
                    'detail': 'No se encontraron menús registrados.',
                    'data': []
                }, status=status.HTTP_200_OK)

            serializer = self.get_serializer(queryset, many=True)
            return Response({
                'success': True,
                'detail': f'Lista de {queryset.count()} menús del día.',
                'data': serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'success': False,
                'detail': 'Ocurrió un error al obtener la lista de menús',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        



class EliminarMenuVista(generics.DestroyAPIView):
    """
    Vista para eliminar un menú del día por su ID.
    """
    queryset = T003MenuDia.objects.all()
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        try:
            menu = self.get_object()  # Busca el menú por ID en la URL
            menu.delete()
            return Response({
                'success': True,
                'detail': 'Menú eliminado correctamente.'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'success': False,
                'detail': 'Ocurrió un error al eliminar el menú',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)