web: python src/manage.py collectstatic --noinput; gunicorn --chdir src/ notif.wsgi --preload
worker: celery --workdir=src/ -A notif.settings worker --concurrency=2 --loglevel=info -n %n@%h