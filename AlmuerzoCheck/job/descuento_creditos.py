from django.db.models import F, Value
from django.db.models.functions import Greatest
from AlmuerzoCheck.models import T001Estudiantes

def aplicar_descuento_credito():
    # Resta 1 a los créditos de todos los estudiantes, pero nunca menor que 0
    T001Estudiantes.objects.update(
        creditos=Greatest(F('creditos') - 1, Value(0))
    )
    
    print("Descuento aplicado correctamente a todos los estudiantes")
