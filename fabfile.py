from fabric.api import local, task, execute, run
import random
import string

import re


@task()
def deploy_to_heroku():
    try:
        app = get_app()
    except:
        app = None
    print("App name: ", app)
    if not app:
        local('git init')
        if is_authenticated():
            local('heroku login')
        if not app:
            create_app()
        set_config()
        add_host(get_app())
        update_requirements_file()
        update_procfile()
        update_production_requirements()
        local('git add -A')
        local('git commit -m "%s" ' % input("Enter commit message: "))
    local('git push heroku master')
    enable_collectstatic()


def is_authenticated():
    text = local('heroku auth:token', True)
    if text == 'not logged in':
        return True
    return False


def get_app():
    app = local('heroku info', True)
    app = re.compile('\w+.[-]*.\w+').findall(app)[0]
    return app


def set_config():
    """Set the heroku config variables"""
    secret_key = generate_key()
    local('heroku config:set SECRET_KEY=%s' % secret_key)
    local('heroku config:set DJANGO_SETTINGS_MODULE=%s' % "notif.settings.production")
    local('heroku config:set DISABLE_COLLECTSTATIC=1')


def generate_key():
    return "".join([random.SystemRandom().choice(string.digits + string.ascii_letters) for i in range(100)])


@task()
def create_app():
    while True:
        try:
            local('heroku create %s' % input("Enter app name: "))
            app = get_app()
            if app:
                break
        except:
            pass


def add_host(app):
    chdir = local('pwd', True)
    file_name = '%s/src/notif/settings/production.py' % chdir
    with open(file_name, "a") as f:
        f.write("ALLOWED_HOSTS += ['%s.herokuapp.com']" % app)


def enable_collectstatic():
    local('heroku config:unset DISABLE_COLLECTSTATIC')


def update_requirements_file():
    local("sed -i '' 's/development/production/g' requirements.txt")


def update_procfile():
    project_name = "notif"
    local("sed -i '' 's/project_name/%s/g' Procfile" % project_name)


def update_production_requirements():
    local("sed -i '' 's/^#.//' requirements/production.txt")

@task()
def set_heroku_env():
    chdir = local('pwd', True)
    filename = "%s/notif/settings/local.env" % chdir
    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if '#' not in line and 'DATABASE_URL' not in line and 'DEBUG' not in line and line.strip():
                local('heroku config:set %s' % line)
