import os


def startDjangoProject(envPath:str, projectName:str, auth:bool) -> bool:
    try:
        COMMAND = f'''mkdir {projectName} & cd {projectName} & django-admin startproject core . & virtualenv env & deactivate & {envPath} & pip install django whitenoise gunicorn & pip freeze > requirements.txt & python manage.py startapp app & cd core & mkdir static & cd static & mkdir css & mkdir js & mkdir images & mkdir fonts'''
        if auth:
            COMMAND = f'''mkdir {projectName} & cd {projectName} & django-admin startproject core . & virtualenv env & deactivate & {envPath} & pip install django whitenoise gunicorn djacc & pip freeze > requirements.txt & python manage.py startapp app & cd core & mkdir static & cd static & mkdir css & mkdir js & mkdir images & mkdir fonts'''
        os.system(COMMAND)
        return True
    except Exception as err:
        print('Project Error: ', err.__class__.__name__)
        return False
