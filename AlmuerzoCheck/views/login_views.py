from rest_framework import generics, status
from rest_framework.response import Response
from AlmuerzoCheck.models import T007UsuariosSistema,T008Acudientes,T001Estudiantes
from AlmuerzoCheck.serializer.AlmuerzoCheck_Serializer import AlmuerzoCheckSerializer,AlmuerzoCheckSerializerLogin,AlmuerzoCheckSerializerListarAdmin,AlmuerzoCheckSerializerUpdate 
from rest_framework.permissions import IsAuthenticated  
from rest_framework.permissions import AllowAny  
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
import random
from django.utils import timezone
from datetime import timedelta

from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from AlmuerzoCheck.serializer.Estudiantes_Serializer import EstudianteSerializer 



class ListarUsuario(generics.ListAPIView):
    queryset = T007UsuariosSistema.objects.all()
    serializer_class = AlmuerzoCheckSerializerListarAdmin
    permission_classes = [IsAuthenticated]  # Asegúrate de que se requiera autenticación

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success': True,
            'detail': 'Lista de personas registradas',
            'data': serializer.data
        }, status=status.HTTP_200_OK)



class CrearUsuario(generics.CreateAPIView):
    queryset = T007UsuariosSistema.objects.all()
    serializer_class = AlmuerzoCheckSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        contrasena = serializer.validated_data.get('password')  # Campo correcto
        if contrasena:
            # Guardar la contraseña como hash
            serializer.validated_data['password'] = make_password(contrasena)
        serializer.save()

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        if T007UsuariosSistema.objects.filter(username=username).exists():
            return Response({
                'success': False,
                'detail': 'El Usuario ya está en uso.',
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response({
            'success': True,
            'detail': 'Usuario creado exitosamente.',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)


# class AutenticacionUsuario(generics.GenericAPIView):
#     serializer_class = AlmuerzoCheckSerializerLogin
#     permission_classes = [AllowAny]  # Permitir a cualquier usuario autenticarse

#     def post(self, request, *args, **kwargs):
#         username = request.data.get('username')
#         contrasena = request.data.get('password')

#         # Validar campos vacíos
#         if not username or not contrasena:
#             return Response({
#                 'success': False,
#                 'detail': 'Usuario y contraseña son requeridos.'
#             }, status=status.HTTP_400_BAD_REQUEST)

#         # Buscar usuario por número de usuario
#         try:
#             usuario = T007UsuariosSistema.objects.get(username=username)
#         except T007UsuariosSistema.DoesNotExist:
#             return Response({
#                 'success': False,
#                 'detail': 'Usuario no encontrado.'
#             }, status=status.HTTP_404_NOT_FOUND)

#         # Comparar contraseñas usando check_password
#         if check_password(contrasena, usuario.password):  # Asegúrate de que este campo es el correcto para la contraseña
#             # Generar tokens JWT
#             refresh = RefreshToken.for_user(usuario)
#             access_token = refresh.access_token

#             return Response({
#                 'detail': 'Login exitoso.',
#                 'data': AlmuerzoCheckSerializerLogin(usuario).data,
#                 'token': str(access_token)
#             }, status=status.HTTP_200_OK)
#         else:
#             return Response({
#                 'success': False,
#                 'detail': 'Contraseña incorrecta.'
#             }, status=status.HTTP_400_BAD_REQUEST)
        





class AutenticacionUsuario(generics.GenericAPIView):
    serializer_class = AlmuerzoCheckSerializerLogin
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        contrasena = request.data.get('password')

        # Validar campos vacíos
        if not username or not contrasena:
            return Response({
                'success': False,
                'detail': 'Usuario y contraseña son requeridos.'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Buscar usuario
        try:
            usuario = T007UsuariosSistema.objects.get(username=username)
        except T007UsuariosSistema.DoesNotExist:
            return Response({
                'success': False,
                'detail': 'Usuario no encontrado.'
            }, status=status.HTTP_404_NOT_FOUND)

        # Verificar contraseña
        if not check_password(contrasena, usuario.password):
            return Response({
                'success': False,
                'detail': 'Contraseña incorrecta.'
            }, status=status.HTTP_400_BAD_REQUEST)

        # ✅ Generar tokens JWT
        refresh = RefreshToken.for_user(usuario)
        access_token = refresh.access_token

        # ✅ Serializar usuario
        usuario_data = AlmuerzoCheckSerializerLogin(usuario).data

        # ✅ Concatenar información del estudiante (si existe)
        if usuario.estudiante:
            estudiante_data = EstudianteSerializer(usuario.estudiante).data
            usuario_data.update({
                "estudiante_info": estudiante_data
            })
        else:
            usuario_data.update({
                "estudiante_info": None
            })

        # ✅ Respuesta final
        return Response({
            'detail': 'Login exitoso.',
            'data': usuario_data,
            'token': str(access_token)
        }, status=status.HTTP_200_OK)
    



    
    
class ActualizarUsuario(generics.UpdateAPIView):
    queryset = T007UsuariosSistema.objects.all()
    serializer_class = AlmuerzoCheckSerializerUpdate
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data.copy()  # Copiamos los datos para modificar

        # Validaciones básicas
        if 'username' in data:
            username = data['username'].strip()
            if not username:
                return Response({'success': False, 'detail': 'El nombre de usuario no puede estar vacío.'},
                                status=status.HTTP_400_BAD_REQUEST)
            # Validar que el username no esté repetido en otro usuario
            if T007UsuariosSistema.objects.filter(username=username).exclude(id=instance.id).exists():
                return Response({'success': False, 'detail': 'El nombre de usuario ya está en uso.'},
                                status=status.HTTP_400_BAD_REQUEST)

        # Hashear la contraseña si se envía
        if 'password' in data and data['password']:
            data['password'] = make_password(data['password'])

        serializer = self.get_serializer(instance, data=data, partial=kwargs.get('partial', False))
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'success': True,
            'detail': 'Usuario actualizado exitosamente.',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    









class RecuperarContrasenaUsuarioCodigo(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')

        if not username:
            return Response({
                'success': False,
                'detail': 'El nombre de usuario es requerido.'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            usuario = T007UsuariosSistema.objects.get(username=username)
        except T007UsuariosSistema.DoesNotExist:
            return Response({
                'success': False,
                'detail': 'No se encontró un usuario con ese nombre.'
            }, status=status.HTTP_404_NOT_FOUND)

        # 🔢 Generar código de recuperación (4 dígitos)
        codigo_recuperacion = random.randint(1000, 9999)

        # ⏰ Guardar código y expiración (2 horas)
        usuario.codigo_recuperacion = str(codigo_recuperacion)
        usuario.codigo_expira = timezone.now() + timedelta(hours=2)
        usuario.save()

        print(f"🔢 Código generado: {codigo_recuperacion} (expira a las {usuario.codigo_expira})")

        # ✉️ Enviar correo electrónico con plantilla HTML
        try:
            template = "recuperar.html"
            context = {
                'Nombre_alerta': "Recuperación de contraseña",
                'codigo': codigo_recuperacion
            }

            html_content = render_to_string(template, context)

            email = EmailMessage(
                subject="Código de recuperación de contraseña",
                body=html_content,
                to=[usuario.correo_electronico]  # se asume que el modelo tiene campo 'email'
            )
            email.content_subtype = 'html'
            email.fail_silently = False
            email.send()

        except Exception as e:
            return Response({
                'success': False,
                'detail': f'Error al enviar el correo: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # ✅ Respuesta exitosa
        return Response({
            'success': True,
            'detail': 'Código de recuperación generado y enviado correctamente.',
            'expira': usuario.codigo_expira,
            # ⚠️ El código solo se devuelve en desarrollo/pruebas, puedes quitarlo en producción
            'codigo_generado': codigo_recuperacion
        }, status=status.HTTP_200_OK)


# class RecuperarContrasenaUsuarioCodigo(generics.GenericAPIView):
#     permission_classes = [AllowAny]

#     def post(self, request, *args, **kwargs):
#         username = request.data.get('username')

#         if not username:
#             return Response({
#                 'success': False,
#                 'detail': 'El nombre de usuario es requerido.'
#             }, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             usuario = T007UsuariosSistema.objects.get(username=username)
#         except T007UsuariosSistema.DoesNotExist:
#             return Response({
#                 'success': False,
#                 'detail': 'No se encontró un usuario con ese nombre.'
#             }, status=status.HTTP_404_NOT_FOUND)

#         # Generar código de 4 dígitos
#         codigo_recuperacion = random.randint(1000, 9999)

#         # Guardar el código y la hora de expiración
#         usuario.codigo_recuperacion = str(codigo_recuperacion)
#         usuario.codigo_expira = timezone.now() + timedelta(hours=2)
#         usuario.save()

#         print(f"🔢 Código generado: {codigo_recuperacion} (expira a las {usuario.codigo_expira})")

#         # Aquí podrías enviar el correo con el código

#         return Response({
#             'success': True,
#             'detail': 'Código de recuperación generado y enviado correctamente.',
#             'codigo_generado': codigo_recuperacion,  # ⚠️ Solo para pruebas
#             'expira': usuario.codigo_expira
#         }, status=status.HTTP_200_OK)


class ActualizarPasswordUsuario(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        nuevo_password = request.data.get('password')
        codigo = request.data.get('codigo')

        if not username or not nuevo_password or not codigo:
            return Response({
                'success': False,
                'detail': 'Debes proporcionar username, password y código.'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            usuario = T007UsuariosSistema.objects.get(username=username)
        except T007UsuariosSistema.DoesNotExist:
            return Response({
                'success': False,
                'detail': 'Usuario no encontrado.'
            }, status=status.HTTP_404_NOT_FOUND)

        # Verificar que el código coincida
        if usuario.codigo_recuperacion != str(codigo):
            return Response({
                'success': False,
                'detail': 'El código de recuperación no es válido.'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Verificar vigencia del código
        if not usuario.codigo_expira or usuario.codigo_expira < timezone.now():
            return Response({
                'success': False,
                'detail': 'El código ha expirado. Solicita uno nuevo.'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Actualizar contraseña
        usuario.password = make_password(nuevo_password)
        usuario.codigo_recuperacion = None
        usuario.codigo_expira = None
        usuario.save()

        return Response({
            'success': True,
            'detail': 'Contraseña actualizada correctamente.'
        }, status=status.HTTP_200_OK)











class EnviarCorreoElectronico(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        correo = request.data.get('correo')
        nombre = request.data.get('nombre')
        subject = request.data.get('asunto')
        mensaje = request.data.get('mensaje')

        if correo and nombre and subject:
            # Configuración del correo electrónico
            template = "alerta.html"
            
            # Crear el contexto para la plantilla
            context = {
                'nombre': nombre,
                'mensaje': mensaje
            }

            # Renderizar la plantilla
            html_content = render_to_string(template, context)

            # Configuración del correo electrónico en formato HTML
            email = EmailMessage()
            email.subject = subject
            email.body = html_content
            email.to = [correo]
            email.content_subtype = 'html'

            try:
                # Enviar el correo electrónico
                email.fail_silently=False
                email.send()
                return Response({'mensaje': 'Correo electrónico enviado correctamente'}, status=status.HTTP_200_OK)
            except Exception as e:
                # Maneja cualquier error al enviar el correo
                return Response({'error': f'Error al enviar el correo: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            # Maneja el caso en el que no se proporciona el correo, el nombre o el asunto
            return Response({'error': 'Por favor, proporciona el correo, el nombre y el asunto.'}, status=status.HTTP_400_BAD_REQUEST)  
        




















class EnviarCorreoElectronicoCodigo(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        correo = request.data.get('correo')
        nombre_alerta = request.data.get('nombre_alerta')  # antes era nombre
        codigo = request.data.get('codigo')
        asunto = request.data.get('asunto', 'Código de verificación')

        # Validar campos requeridos
        if not all([correo, nombre_alerta, codigo]):
            return Response(
                {'error': 'Por favor, proporciona correo, nombre_alerta y codigo.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Cargar la plantilla HTML
        template = "recuperar.html"
        context = {
            'Nombre_alerta': nombre_alerta,
            'codigo': codigo
        }

        # Renderizar contenido HTML
        html_content = render_to_string(template, context)

        # Configurar el correo
        email = EmailMessage(
            subject=asunto,
            body=html_content,
            to=[correo]
        )
        email.content_subtype = 'html'  # importante

        try:
            email.fail_silently = False
            email.send()
            return Response({'mensaje': 'Correo electrónico enviado correctamente'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f'Error al enviar el correo: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)