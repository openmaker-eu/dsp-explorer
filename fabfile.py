from __future__ import with_statement
from fabric.api import *

####################################
########### DJANGO UTILS ###########
####################################

def install():
    local('pip install -r requirements.txt')

def install_static():
    local('python ./manage.py collectstatic')

def check_deploy():
    local('python manage.py check --deploy')

def create_setting():
    local('cp dspexplorer/local_settings.py-example dspexplorer/local_settings.py')

def req_pop():
    local('pip freeze > requirements.txt')

def migrate():
    local('python manage.py migrate')

#fab migrate_app:'APP-NAME'
def migrate_app(app_name):
    local('python manage.py makemigrations %s' % app_name)

def migrate_all():
    local('python manage.py migrate')

def create_superuser():
    local('python manage.py createsuperuser')

def start():
    local('python manage.py runserver 0.0.0.0:8000')

def run_test():
    local('python manage.py test contacts')

