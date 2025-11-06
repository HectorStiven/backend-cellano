from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from .descuento_creditos import aplicar_descuento_credito  # CORRECTO, no "jobs"

scheduler = None

def start():
    global scheduler
    scheduler = BackgroundScheduler()
    trigger = IntervalTrigger(hours=1)
    scheduler.add_job(aplicar_descuento_credito, trigger=trigger)
