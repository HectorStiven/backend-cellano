from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.conf import settings
from AlmuerzoCheck.models import T001Estudiantes
import face_recognition
import numpy as np
import os


class WedCamService(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            foto_subida = request.FILES.get("fotoId")

            if not foto_subida:
                return Response({
                    "success": False,
                    "detail": "Debe enviar una foto."
                }, status=status.HTTP_400_BAD_REQUEST)

            # Cargar la foto enviada y obtener su codificación
            foto_enviada = face_recognition.load_image_file(foto_subida)
            encodings_enviada = face_recognition.face_encodings(foto_enviada)

            if not encodings_enviada:
                return Response({
                    "success": False,
                    "detail": "No se detectó ningún rostro en la imagen enviada."
                }, status=status.HTTP_400_BAD_REQUEST)

            encoding_enviada = encodings_enviada[0]

            # Buscar coincidencia con todos los estudiantes que tengan foto registrada
            estudiantes = T001Estudiantes.objects.exclude(fotoId__isnull=True).exclude(fotoId__exact="")
            mejor_match = None
            mejor_distancia = 1.0

            for estudiante in estudiantes:
                ruta_foto = os.path.join(settings.MEDIA_ROOT, str(estudiante.fotoId))
                if not os.path.exists(ruta_foto):
                    continue

                foto_guardada = face_recognition.load_image_file(ruta_foto)
                encodings_guardada = face_recognition.face_encodings(foto_guardada)

                if not encodings_guardada:
                    continue

                encoding_guardada = encodings_guardada[0]
                distancia = np.linalg.norm(encoding_enviada - encoding_guardada)

                if distancia < 0.6 and distancia < mejor_distancia:
                    mejor_match = estudiante
                    mejor_distancia = distancia

            # Resultado final
            if mejor_match:
                return Response({
                    "success": True,
                    "detail": "Rostro reconocido correctamente.",
                    "data": {
                        "id": mejor_match.id,
                        "identificacion": mejor_match.identificacion,
                        "tipo_documento": mejor_match.tipo_documento,
                        "primer_nombre": mejor_match.primer_nombre,
                        "segundo_nombre": mejor_match.segundo_nombre,
                        "primer_apellido": mejor_match.primer_apellido,
                        "segundo_apellido": mejor_match.segundo_apellido,
                        "genero": mejor_match.genero,
                        "fecha_nacimiento": mejor_match.fecha_nacimiento,
                        "direccion": mejor_match.direccion,
                        "telefono": mejor_match.telefono,
                        "correo": mejor_match.correo,
                        "grado": mejor_match.grado,
                        "grupo": mejor_match.grupo,
                        "jornada": mejor_match.jornada,
                        "año_ingreso": mejor_match.año_ingreso,
                        "estado": mejor_match.estado,
                        "creditos": str(mejor_match.creditos),
                        "creado_en": mejor_match.creado_en,
                        "fotoId": request.build_absolute_uri(mejor_match.fotoId.url) if mejor_match.fotoId else None
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "success": False,
                    "detail": "No se encontró coincidencia con ningún rostro registrado."
                }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({
                "success": False,
                "detail": f"Error interno: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
