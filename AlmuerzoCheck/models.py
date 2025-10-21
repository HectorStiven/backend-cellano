from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


# ============================================================
# MODELO DE BASE DE DATOS - SISTEMA DE CAFETERÍA ESCOLAR
# Autor: DJ Stiven
# Descripción: Gestión de pagos, consumos, menús, inventario,
# sugerencias, acudientes y reportes diarios de almuerzos.
# ============================================================


class T001Estudiantes(models.Model):
    identificacion = models.CharField(max_length=50, unique=True, verbose_name="T001_identificación")
    tipo_documento = models.CharField(max_length=10, help_text="CC, TI, RC, etc.", verbose_name="T001_tipo_documento")
    primer_nombre = models.CharField(max_length=50, verbose_name="T001_primer_nombre")
    segundo_nombre = models.CharField(max_length=50, null=True, blank=True, verbose_name="T001_segundo_nombre")
    primer_apellido = models.CharField(max_length=50, verbose_name="T001_primer_apellido")
    segundo_apellido = models.CharField(max_length=50, null=True, blank=True, verbose_name="T001_segundo_apellido")
    foto = models.CharField(max_length=255, null=True, blank=True, verbose_name="T001_foto")
    genero = models.CharField(max_length=5, help_text="M / F", verbose_name="T001_género")
    fecha_nacimiento = models.DateField(verbose_name="T001_fecha_nacimiento")
    direccion = models.CharField(max_length=200, verbose_name="T001_dirección")
    telefono = models.CharField(max_length=15, verbose_name="T001_teléfono")
    correo = models.EmailField(null=True, blank=True, verbose_name="T001_correo_electrónico")
    grado = models.CharField(max_length=20, verbose_name="T001_grado")
    grupo = models.CharField(max_length=10, verbose_name="T001_grupo")
    jornada = models.CharField(max_length=20, help_text="Mañana, Tarde o Nocturna", verbose_name="T001_jornada")
    año_ingreso = models.IntegerField(verbose_name="T001_año_ingreso")
    estado = models.BooleanField(default=True, verbose_name="T001_estado")
    creditos = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="T001_créditos")
    creado_en = models.DateTimeField(default=timezone.now, verbose_name="T001_creado_en")

    class Meta:
        verbose_name = "Estudiante"
        verbose_name_plural = "Estudiantes"
        db_table = "T001Estudiantes"

    def __str__(self):
        return f"{self.primer_nombre} {self.primer_apellido}"


class T002Pagos(models.Model):
    estudiante = models.ForeignKey(T001Estudiantes, on_delete=models.CASCADE, verbose_name="T002_estudiante")
    mes = models.IntegerField(help_text="1=Enero, 2=Febrero, etc.", verbose_name="T002_mes")
    anio = models.IntegerField(verbose_name="T002_año")
    valor_pagado = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="T002_valor_pagado")
    valor_mensualidad = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="T002_valor_mensualidad")
    fecha_pago = models.DateField(verbose_name="T002_fecha_pago")
    observacion = models.TextField(null=True, blank=True, verbose_name="T002_observación")

    class Meta:
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"
        db_table = "T002Pagos"


class T003MenuDia(models.Model):
    fecha = models.DateField(unique=True, verbose_name="T003_fecha")
    descripcion = models.TextField(verbose_name="T003_descripción")
    plato_principal = models.CharField(max_length=100, verbose_name="T003_plato_principal")
    acompanamiento = models.CharField(max_length=100, verbose_name="T003_acompañamiento")
    bebida = models.CharField(max_length=100, verbose_name="T003_bebida")
    postre = models.CharField(max_length=100, verbose_name="T003_postre")
    calorias_total = models.IntegerField(verbose_name="T003_calorías_total")

    class Meta:
        verbose_name = "Menú del Día"
        verbose_name_plural = "Menús del Día"
        db_table = "T003MenuDia"

    def __str__(self):
        return f"Menú {self.fecha} - {self.plato_principal}"


class T004Consumos(models.Model):
    estudiante = models.ForeignKey(T001Estudiantes, on_delete=models.CASCADE, verbose_name="T004_estudiante")
    menu = models.ForeignKey(T003MenuDia, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="T004_menú")
    fecha = models.DateField(default=timezone.now, verbose_name="T004_fecha")
    hora = models.TimeField(default=timezone.now, verbose_name="T004_hora")
    repetido = models.BooleanField(default=False, verbose_name="T004_repetido")
    reclamado = models.BooleanField(default=False, verbose_name="T004_reclamado")

    class Meta:
        verbose_name = "Consumo"
        verbose_name_plural = "Consumos"
        db_table = "T004Consumos"


class T005Sugerencias(models.Model):
    estudiante = models.ForeignKey(T001Estudiantes, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="T005_estudiante")
    menu = models.ForeignKey(T003MenuDia, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="T005_menú")
    comentario = models.TextField(verbose_name="T005_comentario")
    calificacion = models.IntegerField(help_text="Puntaje de 1 a 5", verbose_name="T005_calificación")
    fecha = models.DateTimeField(default=timezone.now, verbose_name="T005_fecha")

    class Meta:
        verbose_name = "Sugerencia"
        verbose_name_plural = "Sugerencias"
        db_table = "T005Sugerencias"


class T006Parametros(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="T006_nombre")
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="T006_valor")
    descripcion = models.TextField(null=True, blank=True, verbose_name="T006_descripción")

    class Meta:
        verbose_name = "Parámetro"
        verbose_name_plural = "Parámetros"
        db_table = "T006Parametros"


class T007UsuariosSistema(AbstractBaseUser, PermissionsMixin):

    ROLES_OPCIONES = [
        ('admin', 'Administrador'),
        ('empleado', 'Empleado'),
        ('estudiante', 'Estudiante'),
    ]

    username = models.CharField(max_length=100, unique=True, verbose_name="T007_username")
    password = models.CharField(max_length=200, verbose_name="T007_password")
    rol = models.CharField(max_length=20, choices=ROLES_OPCIONES, default='estudiante', help_text="admin | empleado | estudiante", verbose_name="T007_rol")
    estudiante = models.ForeignKey(T001Estudiantes, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="T007_estudiante")
    creado_en = models.DateTimeField(default=timezone.now, verbose_name="T007_creado_en")
    correo_electronico = models.EmailField(null=True, blank=True, verbose_name="T007_correo_electrónico")
    
   

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = [ "password", "correo_electronico" ]

    class Meta:
        verbose_name = "Usuario del Sistema"
        verbose_name_plural = "Usuarios del Sistema"
        db_table = "T007UsuariosSistema"



class T008Acudientes(models.Model):
    estudiante = models.ForeignKey(T001Estudiantes,on_delete=models.CASCADE,verbose_name="T008_estudiante",related_name="acudientes")
    nombre = models.CharField(max_length=100, verbose_name="T008_nombre")
    telefono = models.CharField(max_length=15, verbose_name="T008_telefono", null=True, blank=True)
    correo = models.EmailField(verbose_name="T008_correo", null=True, blank=True)
    parentesco = models.CharField(max_length=50, verbose_name="T008_parentesco", null=True, blank=True)
    direccion = models.CharField(max_length=200, verbose_name="T008_direccion", null=True, blank=True)
    fecha_nacimiento = models.DateField(verbose_name="T008_fecha_nacimiento", null=True, blank=True)
    ocupacion = models.CharField(max_length=100, verbose_name="T008_ocupacion", null=True, blank=True)
    estado = models.BooleanField(default=True, verbose_name="T008_estado")
    observacion = models.TextField(null=True, blank=True, verbose_name="T008_observacion")
    creado_en = models.DateTimeField(default=timezone.now, verbose_name="T008_creado_en")

    class Meta:
        verbose_name = "Acudiente"
        verbose_name_plural = "Acudientes"
        db_table = "T008Acudientes"

