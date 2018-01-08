import os

from kombu import Queue, Exchange

ADMINS = [
    ('Rohan', 'rohan@rohanroy.com')
]

REDIS_HOST = os.environ.get('REDIS_HOSTNAME', 'localhost')

RABBIT_HOSTNAME = os.environ.get('RABBIT_HOSTNAME', 'localhost')

if RABBIT_HOSTNAME.startswith('tcp://'):
    RABBIT_HOSTNAME = RABBIT_HOSTNAME.split('//')[1]

BROKER_URL = os.environ.get('BROKER_URL', '')

if not BROKER_URL:
    BROKER_URL = 'amqp://{user}:{password}@{hostname}/{vhost}'.format(
        user=os.environ.get('RABBITMQ_DEFAULT_USER', ''),
        password=os.environ.get('RABBITMQ_DEFAULT_PASS', ''),
        hostname=RABBIT_HOSTNAME,
        vhost=os.environ.get('RABBIT_ENV_VHOST', ''))

# We don't want to have dead connections stored on rabbitmq, so we have to negotiate using heartbeats
# BROKER_HEARTBEAT = os.environ.get('BROKER_HEARTBEAT')
# if not BROKER_URL.endswith(BROKER_HEARTBEAT):
#     BROKER_URL += BROKER_HEARTBEAT


# Celery configuration
# configure queues, currently we have only one
CELERY_DEFAULT_QUEUE = os.environ.get('CELERY_DEFAULT_QUEUE')
CELERY_QUEUES = (
    Queue(CELERY_DEFAULT_QUEUE, Exchange(CELERY_DEFAULT_QUEUE), routing_key=CELERY_DEFAULT_QUEUE),
    Queue('transient', Exchange('transient', delivery_mode=1), routing_key='transient', durable=False),
)

# Sensible settings for celery
CELERY_ALWAYS_EAGER = False
CELERY_ACKS_LATE = True
CELERY_TASK_PUBLISH_RETRY = True
CELERY_DISABLE_RATE_LIMITS = False

# By default we will ignore result
# If you want to see results and try out tasks interactively, change it to False
# Or change this setting on tasks level
CELERY_IGNORE_RESULT = True
CELERY_SEND_TASK_ERROR_EMAILS = True
CELERY_TASK_RESULT_EXPIRES = 600

# Set redis as celery result backend
REDIS_PORT = os.environ.get('REDIS_PORT', '6379')
REDIS_DB = os.environ.get('REDIS_DB', '0')
CELERY_RESULT_BACKEND = 'redis://%s:%d/%d' % (REDIS_HOST, int(REDIS_PORT), int(REDIS_DB))
# Don't use pickle as serializer, json is much safer
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['application/json']

CELERYD_HIJACK_ROOT_LOGGER = False
CELERYD_PREFETCH_MULTIPLIER = 1
CELERYD_MAX_TASKS_PER_CHILD = 1000

BROKER_POOL_LIMIT = 1000
# CELERY_REDIS_MAX_CONNECTIONS = 2000
BROKER_CONNECTION_TIMEOUT = 10
CELERYD_TASK_SOFT_TIME_LIMIT = 60