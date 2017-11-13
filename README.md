# DSP Explorer - Open Maker Project

Django Application, frontend project of OpenMaker Digital Social Platform.


## Requirements

First of all you need to have:

    Python 2.7+
    mySql or Postgresql
    nodejs / npm / sass

To ensure a stable and indipendent environment, use **virtualenv** (execute this command inside the root folder):

    pip install virtualenv
    virtualenv -p /usr/bin/python2.7 env
    source env/bin/activate

To enable faster development and configuration we're using **fabric**:

    pip install fabric

To install the application

    fab install
    OR
    pip install -r requirements.txt
    npm install

Configure your local setting file:

    fab create_setting
    Edit the file dspexplorer/local_settings.py with your local configuration

Migration:

    fab migrate

Start server:

    fab start

Create a super user

    fab create_superuser

Open your browser on **http://localhost:8000** and here we go!

## Production

Install all the requirements. After the installation create a virtualhost like:

    <VirtualHost *:80>

          ServerName dsp.openmaker.eu
          ServerAdmin hackademy@top-ix.org
    
          WSGIScriptAlias / /var/www/dsp-explorer/dspexplorer/wsgi.py
          WSGIDaemonProcess DSPEXPLORER python-path=/var/www/dsp-explorer:/var/www/envExplorer/lib/python2.7/site-packages
          WSGIProcessGroup DSPEXPLORER
          
          DocumentRoot /var/www/dsp-explorer
          Alias /static/ /var/www/dsp-explorer/static_root/
          
      <Directory /var/www/dsp-explorer/>
          Options ExecCGI MultiViews Indexes
          MultiViewsMatch Handlers
          AddHandler wsgi-script .py
          AddHandler wsgi-script .wsgi
          DirectoryIndex index.html index.py app.wsgi
          Order allow,deny
          Require all granted
          Allow from all
      </Directory>
      
          ErrorLog ${APACHE_LOG_DIR}/dspexplorer-error.log
          CustomLog ${APACHE_LOG_DIR}/dspexplorer-access.log combined
    </VirtualHost>

## Release - Automatic

We've created an automatic task to prepare for release the code, just simply run:

    fab release:'RELEASE-COMMIT-MESSAGE'
    
This task will merge automatically all the changes in the release branch, run **npm run prod** and **fab install_static**.
After minification and static files installation will commit and push the changes.

On the production server we just need to pull!

## Release - Manually

Install static files:

    npm run prod
    
Copy static files on Apache Alias:

    fab install_static

Here we go!

