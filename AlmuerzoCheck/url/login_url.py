from django.urls import path
from AlmuerzoCheck.views import login_views
from AlmuerzoCheck.views import acudiente
from AlmuerzoCheck.views import estudiantes
from AlmuerzoCheck.views import menu
from AlmuerzoCheck.views import WedcamId
from AlmuerzoCheck.views import consumos
from AlmuerzoCheck.views import Sugerencias
from AlmuerzoCheck.views import Pago
urlpatterns = [
    path('usuarios/', login_views.ListarUsuario.as_view(), name='listar-usuarios'),
    path('usuarios/crear/', login_views.CrearUsuario.as_view(), name='crear-usuario'),
    path('usuarios/autenticacion/', login_views.AutenticacionUsuario.as_view(), name='autenticacion_usuario'),
    path('usuarios/actualizar/<int:pk>/', login_views.ActualizarUsuario.as_view(), name='actualizar-usuario'),  #solo admin

    # path('usuarios/eliminar/<int:pk>/', login_views.EliminarUsuario.as_view(), name='eliminar-usuario'),  pendiente tiene es que desactivarlo no eliminarlo
    path('usuarios/recuperar_contrasena/', login_views.RecuperarContrasenaUsuarioCodigo.as_view(), name='recuperar-contrasena-usuario'),
    path('usuarios/actualizar_contrasena/', login_views.ActualizarPasswordUsuario.as_view(), name='actualizar-contrasena-usuario'),

    path('usuarios/correo_disponible/', login_views.EnviarCorreoElectronico.as_view(), name='verificar-correo-disponible'),
    path('usuarios/enviar_correo/', login_views.EnviarCorreoElectronicoCodigo.as_view(), name='enviar-correo-electronico'),

    #CREAR ACUDIENTE PARA ESTUDIANTE
    path('usuarios/crear_acudiente/', acudiente.CrearAcudienteVista.as_view(), name='crear-acudiente-para-estudiante'),
    path('usuarios/listar_acudientes/<int:estudiante_id>/', acudiente.ListarAcudientesVista.as_view(), name='listar-acudientes'),
    path('usuarios/actualizar_acudiente/<int:pk>/', acudiente.ActualizarAcudienteVista.as_view(), name='actualizar-acudiente'),
    path('usuarios/borrar_acudiente/<int:pk>/', acudiente.BorrarAcudienteVista.as_view(), name='borrar-acudiente'),


    path('usuarios/crear_estudiante/', estudiantes.CrearEstudianteVista.as_view(), name='crear-estudiante'),
    path('usuarios/listar_estudiantes/', estudiantes.ListarEstudiantesVista.as_view(), name='listar-estudiantes'),
    path('usuarios/editar_estudiante/<int:pk>/', estudiantes.EditarEstudianteVista.as_view(), name='editar-estudiante'),
    path('usuarios/obtener_estudiante/<int:pk>/', estudiantes.ObtenerEstudianteInfo.as_view(), name='obtener-estudiante-info'),
    
   path('menu/crear/', menu.CrearMenuVista.as_view(), name='crear-menu'),
   path('menu/listar/', menu.ListarMenuVista.as_view(), name='listar-menu'),
   path('menu/eliminar/<int:pk>/', menu.EliminarMenuVista.as_view(), name='eliminar-menu'),



  # path('webcam/service/', WedcamId.WedCamService.as_view(), name='wedcam-service'),
  path('webcam/manual/', WedcamId.BuscarEstudianteManual.as_view(), name='wedcam-test'),



  path('consumos/crear/', consumos.CrearConsumoVista.as_view(), name='crear-consumo'),
  path('consumos/estudiante/<int:estudiante_id>/', consumos.ListarConsumosPorEstudianteVista.as_view(), name='listar-consumos-por-estudiante'),
  path('consumos/listar_todos/', consumos.ListarConsumosPorFechaVista.as_view(), name='listar-todos-los-consumos'),

  path('sugerencias/crear/', Sugerencias.CrearSugerenciaVista.as_view(), name='crear-sugerencia'),
  path('sugerencias/eliminar/<int:pk>/', Sugerencias.EliminarSugerenciaVista.as_view(), name='eliminar-sugerencia'),
  path('sugerencias/listar/', Sugerencias.ListarSugerenciasVista.as_view(), name='listar-sugerencias'),


  path('pagos/crear/', Pago.CrearPagoVista.as_view(), name='crear-pago'),
  path('pagos/listar/', Pago.ListarPagosPorMesAnioVista.as_view(), name='listar-pagos'),

]
