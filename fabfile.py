from __future__ import with_statement
from fabric.api import *

####################################
# DJANGO UTILS                     #
####################################


def install():
    local('pip install -r requirements.txt')
    local('npm i')


def install_static():
    local('python ./manage.py collectstatic')


def check_deploy():
    local('python manage.py check --deploy')


def create_setting():
    local('cp dspexplorer/local_settings.py-example dspexplorer/local_settings.py')


def req_pop():
    local('pip freeze > requirements.txt')


def makemigrations():
    local('python manage.py makemigrations')


def migrate():
    local('python manage.py migrate')


# fab migrate_app:'APP-NAME'
def migrate_app(app_name):
    local('python manage.py makemigrations %s' % app_name)


def create_superuser():
    local('python manage.py createsuperuser')


def start():
    local('npm run dev &')
    local('python manage.py runserver 0.0.0.0:8000')


@hosts(['topix@dspexplorer.top-ix.org'])
def deploy_dev():
    with cd('/var/www/dsp-explorer'):
        run('git checkout .')
        run('git pull')
        run('npm run prod')
        run('service apache2 reload')
