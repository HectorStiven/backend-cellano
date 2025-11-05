from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

from AlmuerzoCheck.models import T004Consumos, T001Estudiantes, T003MenuDia, T008Acudientes
from AlmuerzoCheck.serializer.Consumos_Serializer import ConsumosSerializer, ConsumoSerializer, EstudianteSinConsumoSerializer



# class CrearConsumoVista(generics.CreateAPIView):
#     queryset = T004Consumos.objects.all()
#     serializer_class = ConsumosSerializer

#     def create(self, request, *args, **kwargs):
#         try:
#             serializer = self.get_serializer(data=request.data)
#             serializer.is_valid(raise_exception=True)
#             serializer.save()

#             return Response({
#                 'success': True,
#                 'detail': 'Consumo registrado correctamente',
#                 'data': serializer.data
#             }, status=status.HTTP_201_CREATED)

#         except ValidationError as e:
#             raise ValidationError(e.detail)
#         except Exception as e:
#             return Response({
#                 'success': False,
#                 'detail': 'Error al registrar el consumo',
#                 'error': str(e)
#             }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class CrearConsumoVista(generics.CreateAPIView):
    queryset = T004Consumos.objects.all()
    serializer_class = ConsumosSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            consumo = serializer.save()

            # --- Datos del consumo creado ---
            estudiante = consumo.estudiante
            menu = consumo.menu
            fecha = consumo.fecha.strftime("%Y-%m-%d")
            hora = consumo.hora.strftime("%H:%M:%S")

            # --- Buscar acudiente (si existe) ---
            acudiente = T008Acudientes.objects.filter(estudiante=estudiante).first()
            correo_destino = acudiente.correo if acudiente and acudiente.correo else estudiante.correo

            if correo_destino:
                # --- Preparar datos para la plantilla ---
                context = {
                    "nombre": estudiante.primer_nombre,
                    "apellido": estudiante.primer_apellido,
                    "fecha": fecha,
                    "hora": hora,
                    "menu": f"{menu.plato_principal} con {menu.acompanamiento}, {menu.bebida} y {menu.postre}"
                }

                # --- Renderizar HTML del correo ---
                html_content = render_to_string("informe_consumo.html", context)

                # --- Enviar correo ---
                email = EmailMessage(
                    subject=f"Informe del almuerzo de {estudiante.primer_nombre} {estudiante.primer_apellido}",
                    body=html_content,
                    from_email=getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@colegio.com"),
                    to=[correo_destino],
                )
                email.content_subtype = "html"
                email.fail_silently = False
                email.send()

            return Response({
                'success': True,
                'detail': 'Consumo registrado y correo enviado correctamente',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                'success': False,
                'detail': 'Error al registrar el consumo o enviar el correo',
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
        

from datetime import datetime
from AlmuerzoCheck.models import T001Estudiantes











class ListarConsumosPorFechaVista(generics.ListAPIView):
    serializer_class = ConsumoSerializer  # Para consumos existentes

    def get_queryset(self):
        # Leer datos de query params
        fecha_str = self.request.query_params.get('fecha')
        sin_registro = self.request.query_params.get('sin_registro', 'true').lower() == 'true'

        if not fecha_str:
            raise ValidationError("No se proporcionó la fecha. Use 'YYYY-MM-DD' como query param.")

        try:
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        except ValueError:
            raise ValidationError("Formato de fecha inválido. Use 'YYYY-MM-DD'.")

        if sin_registro:
            # Mostrar consumos existentes, un registro por estudiante
            queryset = (
                T004Consumos.objects
                .filter(fecha=fecha)
                .order_by('estudiante_id')  # necesario para distinct
                .distinct('estudiante_id')
            )
        else:
            # Mostrar estudiantes sin consumos ese día
            consumos_estudiantes = T004Consumos.objects.filter(fecha=fecha).values_list('estudiante_id', flat=True)
            queryset = T001Estudiantes.objects.exclude(id__in=consumos_estudiantes)
        
        return queryset, sin_registro

    def get(self, request, *args, **kwargs):
        try:
            queryset, sin_registro = self.get_queryset()

            if not queryset.exists():
                return Response({
                    'success': True,
                    'detail': 'No hay registros encontrados',
                    'data': []
                }, status=status.HTTP_200_OK)

            # Serializar según el caso
            if sin_registro:
                serializer = self.get_serializer(queryset, many=True)
            else:
                serializer = EstudianteSinConsumoSerializer(queryset, many=True, context={'request': request})

            return Response({
                'success': True,
                'detail': 'Lista de registros',
                'count': queryset.count(),
                'data': serializer.data
            }, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response({
                'success': False,
                'detail': str(e),
                'data': []
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'success': False,
                'detail': 'Ocurrió un error al obtener los consumos',
                'error': str(e),
                'data': []
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)