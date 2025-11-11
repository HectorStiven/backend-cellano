from django.db.models import F, Value, Q
from django.db.models.functions import Greatest
from AlmuerzoCheck.models import T001Estudiantes


def aplicar_descuento_credito():
    try:
        # 🧾 1️⃣ Descontar 1 crédito (sin bajar de 0)
        estudiantes_afectados = T001Estudiantes.objects.update(
            creditos=Greatest(F('creditos') - 1, Value(0))
        )

        print(f"✅ Se aplicó el descuento de créditos a {estudiantes_afectados} estudiantes.")

        # 🧮 2️⃣ Cambiar el estado a False donde los créditos quedaron en 0
        estudiantes_inactivos = T001Estudiantes.objects.filter(creditos__lte=0, estado=True).update(estado=False)

        if estudiantes_inactivos > 0:
            print(f"⚠️ {estudiantes_inactivos} estudiantes pasaron a estado inactivo (sin créditos).")
        else:
            print("✅ No hay estudiantes con créditos igual a 0 que requieran cambio de estado.")

        print("🎯 Descuento y actualización de estado completados correctamente.")

    except Exception as e:
        print(f"💥 [ERROR] Ocurrió un problema al aplicar el descuento: {str(e)}")
