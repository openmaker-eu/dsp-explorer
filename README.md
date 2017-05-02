# DSP Explorer - Open Maker Project

Django Application, frontend project of OpenMaker Digital Social Platform.

## Requirements

First of all you need to have:

    Python 2.7+
    mySql or Postgresql

To ensure a stable and indipendent environment, use **virtualenv** (execute this command inside the root folder):

    pip install virtualenv
    virtualenv env
    source env/bin/activate

To enable faster development and configuration we're using **fabric**:

    pip install fabric

To install the application

    fab install
    OR
    pip install -r requirements.txt

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
