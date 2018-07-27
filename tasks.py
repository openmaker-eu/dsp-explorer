from invoke import task, Collection
# USAGE: invoke run [function_name]

@task
def start(c):
    c.run('npm run dev & python manage.py runserver 0.0.0.0:8000')

@task
def init(c, colored=True):
    c.run('python manage.py migrate')
    c.run('python ./manage.py loaddata --ignorenonexistent db.json')
    c.run('npm run dev & python manage.py runserver 0.0.0.0:8000')

@task
def dumpdata(c):
    c.run('python ./manage.py dumpdata > db.json --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 4')

@task
def loaddata(c):
    c.run('python ./manage.py loaddata --ignorenonexistent db.json ')

@task
def createsetting(c):
    c.run('cp dspexplorer/c.run_settings.py-example dspexplorer/c.run_settings.py')

@task
def freeze(c):
    c.run('pip freeze > requirements.txt')

@task
def makemigrations(c):
    c.run('python manage.py makemigrations')

@task
def migrate(c):
    c.run('python manage.py migrate')

@task
def install(c):
    c.run('pip install -r requirements.txt')
    c.run('npm install')

@task
def installstatic(c):
    c.run('python ./manage.py collectstatic')

@task
def test(c, filename=''):
    c.run('python manage.py test %s -k' % filename)

@task
def test_e2e(c):
    c.run('protractor protractor-conf.js')
