from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from .descuento_creditos import aplicar_descuento_credito  # CORRECTO, no "jobs"

scheduler = None

def start():
    global scheduler
    scheduler = BackgroundScheduler()
    trigger = IntervalTrigger(seconds=1)  # Ejecutar cada 10 segundos
    # scheduler.add_job(aplicar_descuento_credito, trigger=trigger)
    scheduler.start()
