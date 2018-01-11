from __future__ import absolute_import

import requests

from notif.settings.celery_app import app


@app.task(bind=True, default_retry_delay=10)  # set a retry delay, 10 equal to 10s
def longtime_add(self, i):
    print('long time task begins')
    try:
        print("url: ", i)
        r = requests.get(i)
        print("status: ", r.status_code)
        print('long time task finished')
    except Exception as exc:
        raise self.retry(exc=exc)
    return r.status_code


@app.task(time_limit=10)
def add(x, y):
    return x + y
