from rest_framework import serializers
from AlmuerzoCheck.models import T007UsuariosSistema, T001Estudiantes


# ✅ Serializer para crear usuarios
class AlmuerzoCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = T007UsuariosSistema
        fields = [
            'username', 
            'password',
            'estudiante',
        ]
        extra_kwargs = {
            'password': {'write_only': True}  # Evita mostrar la contraseña en las respuestas
        }


# ✅ Serializer para login o mostrar usuario
class AlmuerzoCheckSerializerLogin(serializers.ModelSerializer):
    class Meta:
        model = T007UsuariosSistema
        fields = ['id', 'last_login', 'username', 'rol', 'creado_en', 'estudiante']

class AlmuerzoCheckSerializerListarAdmin(serializers.ModelSerializer):
    class Meta:
        model = T007UsuariosSistema
        fields = "__all__"
class EstudianteSerializer(serializers.ModelSerializer):
    class Meta:
        model = T001Estudiantes
        fields = '__all__'  # Trae todos los campos del estudiante

class UsuarioSistemaSerializer(serializers.ModelSerializer):
    estudiante_info = EstudianteSerializer(source='estudiante', read_only=True)

    class Meta:
        model = T007UsuariosSistema
        fields = [
            'id',
            'username',
            'rol',
            'correo_electronico',
            'creado_en',
            'estudiante',
            'estudiante_info',  # Campo anidado
        ]

class AlmuerzoCheckSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = T007UsuariosSistema
        fields =  ['id', 'username', 'rol', 'creado_en']