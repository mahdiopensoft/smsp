import os
from decouple import config
from celery import Celery
from config.settings.sync_setting import SYSTEM_ID
from kombu import Exchange, Queue

FINANCE_COMMANDS_EXCHANGE = Exchange("finance.commands", "topic",durable=True,auto_delete=False)
FINANCE_EVENTS_EXCHANGE = Exchange("finance.events", "topic",durable=True,auto_delete=False)


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
app_integration = Celery(
    main=f"{SYSTEM_ID}_integration",
    broker=config('CELERY_BROKER_URL', default='amqp://guest:guest@127.0.0.1:5672/'),
    backend=config('CELERY_RESULT_BACKEND', default='rpc://'),
)
app_integration.config_from_object('django.conf:settings', namespace='CELERY')
app_integration.conf.task_queues = (
    Queue(
        f"{SYSTEM_ID}.events",
        FINANCE_EVENTS_EXCHANGE,
        routing_key=f"{SYSTEM_ID}.#",
        durable=True,
        exclusive=False,
        auto_delete=False
    ),
)
app_integration.conf.task_create_missing_queues=True
app_integration.autodiscover_tasks()

@app_integration.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

