web: python src/manage.py collectstatic --noinput; gunicorn --chdir src/ notif.wsgi --preload
worker: celery --workdir=src/ -A notif.settings worker --concurrency=20 --loglevel=info -n %n@%h