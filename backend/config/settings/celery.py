
# اعدادات Celery مع RabbitMQ

# CELERY_TASK_ALWAYS_EAGER = False
#
# CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
# CELERY_BROKER_URL = 'amqp://guest:guest@127.0.0.1:5672//'
# # CELERY_BROKER_URL = 'amqp://guest:guest@127.0.0.1:5672/uds_vhost'
#
# CELERY_ACCEPT_CONTENT = ['json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'
# CELERY_TIMEZONE = 'Asia/Riyadh'
#
# CELERY_REDIS_BACKEND_USE_SSL = False
# CELERY_REDIS_SOCKET_TIMEOUT = 20
# CELERY_REDIS_RETRY_ON_TIMEOUT = True
#
# CELERY_TASK_DEFAULT_QUEUE = 'uds_local_queue'
# CELERY_WORKER_NODE_NAME = "uds_worker@%h"

from kombu import Exchange, Queue
#
# SYSTEM_ID = "uds_central"
#
# FINANCE_COMMANDS_EXCHANGE = Exchange("finance.commands", "topic")
# FINANCE_EVENTS_EXCHANGE = Exchange("finance.events", "topic")
#
# CELERY_TASK_QUEUES = (
#     Queue(
#         f"{SYSTEM_ID}.events",
#         FINANCE_EVENTS_EXCHANGE,
#         routing_key=f"{SYSTEM_ID}.#",
#     ),
# )
#
#
# CELERY_BROKER_URL = 'amqp://guest:guest@127.0.0.1:5672//'
# CELERY_RESULT_BACKEND = 'rpc://' # django-db after install the required package django-celery-results
# CELERY_TASK_DEFAULT_EXCHANGE = FINANCE_COMMANDS_EXCHANGE
# CELERY_TASK_DEFAULT_TYPE = "topic"
#
# CELERY_BROKER_HEARTBEAT = 600
# CELERY_BROKER_CONNECTION_TIMEOUT = 300
# CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
#
# CELERY_WORKER_PREFETCH_MULTIPLIER = 1
