'''
Fabfile for toptal todo project

Example
=======

    $ fab deploy

* python manage.py runserver --> http://127.0.0.1:8000/ping --> pong
'''

from fabric.api import env, task, cd, local

env.PIP = "~/venv/talon/bin/pip"
env.PYTHON = "~/venv/talon/bin/python"

@task
def init_deploy():
    """
    Setup heroku environment and make first deploy
    """
    local('wget -qO- https://toolbelt.heroku.com/install-ubuntu.sh | sh')
    local('heroku create')
    local('git push heroku master')
    local('heroku ps:scale web=1')
    local('heroku run python manage.py syncdb')
    local('heroku run python manage.py migrate')
    local('heroku addons:add mandrill')

@task
def deploy():
    """
    Deploy application to heroku
    """
    local('git push heroku master')
    local('heroku open')

@task
def log():
    """
    Print worker logs and status
    """
    local('heroku logs')
    local('heroku ps')


@task
def setup_local_env():
    """
    Setup virtual environment for developers
    """
    local("mkdir  ~/venv")
    with cd("~/venv"):
        local("virtualenv --no-site-packages talon")
    local("mkdir  ~/workspace")
    with cd("~/workspace"):
        local("git clone https://github.com/"\
              "Toptal-screening/project-artem-mezhenin")
    with cd("~/workspace/project-artem-mezhenin"):
        local(env.PIP + " install -r requirements.txt")
        local("touch settings_local.py")
        local(env.PYTHON + " manage.py syncdb")
        local(env.PYTHON + " manage.py migrate")

