from rest_framework import serializers
from AlmuerzoCheck.models import T007UsuariosSistema


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

class AlmuerzoCheckSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = T007UsuariosSistema
        fields =  ['id', 'username', 'rol', 'creado_en']