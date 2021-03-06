from __future__ import absolute_import

import logging
import os

import celery
import raven
from django.conf import settings
from kombu import serialization
from raven.contrib.celery import register_signal, register_logger_signal

logger = logging.getLogger(__name__)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notif.settings.development')

# Sentry settings
SENTRY_LINK = "https://" + settings.RAVEN_CLIENT_ID + ":" + \
              settings.RAVEN_CLIENT_SECRET + "@app.getsentry.com/" + settings.APP_ID


class Celery(celery.Celery):
    def on_configure(self):
        client = raven.Client(SENTRY_LINK)

        # register a custom filter to filter out duplicate logs
        register_logger_signal(client)

        # hook into the Celery error handler
        register_signal(client)


# set the default Django settings module for the 'celery' program.
serialization.registry._decoders.pop("application/x-python-serialize")

app = Celery('notif.settings', broker=settings.BROKER_URL, backend=settings.CELERY_RESULT_BACKEND,
             include=['notif.settings.celery_tasks'])

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.task_reject_on_worker_lost = True
app.conf.task_acks_late = True

if __name__ == '__main__':
    app.start()
