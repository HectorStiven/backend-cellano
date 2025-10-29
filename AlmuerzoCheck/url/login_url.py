from django.urls import path
from AlmuerzoCheck.views import login_views
from AlmuerzoCheck.views import acudiente
from AlmuerzoCheck.views import estudiantes
from AlmuerzoCheck.views import menu
from AlmuerzoCheck.views import WedcamId

urlpatterns = [
    path('usuarios/', login_views.ListarUsuario.as_view(), name='listar-usuarios'),
    path('usuarios/crear/', login_views.CrearUsuario.as_view(), name='crear-usuario'),
    path('usuarios/autenticacion/', login_views.AutenticacionUsuario.as_view(), name='autenticacion_usuario'),
    path('usuarios/actualizar/<int:pk>/', login_views.ActualizarUsuario.as_view(), name='actualizar-usuario'),  #solo admin


    # path('usuarios/eliminar/<int:pk>/', login_views.EliminarUsuario.as_view(), name='eliminar-usuario'),  pendiente tiene es que desactivarlo no eliminarlo
    path('usuarios/recuperar_contrasena/', login_views.RecuperarContrasenaUsuarioCodigo.as_view(), name='recuperar-contrasena-usuario'),
    path('usuarios/actualizar_contrasena/', login_views.ActualizarPasswordUsuario.as_view(), name='actualizar-contrasena-usuario'),

    path('usuarios/correo_disponible/', login_views.EnviarCorreoElectronico.as_view(), name='verificar-correo-disponible'),


    #CREAR ACUDIENTE PARA ESTUDIANTE
    path('usuarios/crear_acudiente/', acudiente.CrearAcudienteVista.as_view(), name='crear-acudiente-para-estudiante'),
    path('usuarios/listar_acudientes/<int:estudiante_id>/', acudiente.ListarAcudientesVista.as_view(), name='listar-acudientes'),
    path('usuarios/actualizar_acudiente/<int:pk>/', acudiente.ActualizarAcudienteVista.as_view(), name='actualizar-acudiente'),
    path('usuarios/borrar_acudiente/<int:pk>/', acudiente.BorrarAcudienteVista.as_view(), name='borrar-acudiente'),


    path('usuarios/crear_estudiante/', estudiantes.CrearEstudianteVista.as_view(), name='crear-estudiante'),
    path('usuarios/listar_estudiantes/', estudiantes.ListarEstudiantesVista.as_view(), name='listar-estudiantes'),

   path('menu/crear/', menu.CrearMenuVista.as_view(), name='crear-menu'),
   path('menu/listar/', menu.ListarMenuVista.as_view(), name='listar-menu'),
   path('menu/eliminar/<int:pk>/', menu.EliminarMenuVista.as_view(), name='eliminar-menu'),



  path('wedcam/service/', WedcamId.WedCamService.as_view(), name='wedcam-service'),
]