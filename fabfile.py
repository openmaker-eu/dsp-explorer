# -*- coding: utf-8 -*-
from __future__ import with_statement
from fabric import *


def check_deploy():
    local('python manage.py check --deploy')


def create_superuser():
    local('python manage.py createsuperuser')


# @hosts(['topix@dspexplorer.top-ix.org'])
# def deploy_dev():
#     with cd('/var/www/dsp-explorer'):
#         run('git checkout .')
#         run('git pull')
#         run('npm run prod')
#         run('fab install_static')
#         run('service apache2 reload')
#
#
# @hosts(['topix@dspexplorer.top-ix.org'])
# def deploy_branch(branch):
#     with cd('/var/www/dsp-explorer'):
#         run('git checkout %s' % branch)
#         run('git pull')
#         run('fab install')
#         run('fab migrate')
#         run('npm run prod')
#         run('fab install_static')
#         run('service apache2 reload')


# fab release:'RELEASE-COMMIT-MESSAGE'
def release(message):
    local('git checkout release')
    local('git merge master')
    local('npm install')
    local('npm run prod')
    local('fab install_static')
    #local('git commit -am "%s"' % message)
    local('git push')
    local('git checkout master')


def pair_crm_ids():
    local('python ./capsule_crm.py pair_crm_ids')


