import os


confSettings = """
# Added by Auto-mated script...

import os
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'core/static')]

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


EMAIL_FROM_USER = 'DexterSol'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = "justcrawlera@gmail.com" # testing
EMAIL_HOST_PASSWORD = "jfmchfxgsebszbip" # testing

LOGIN_URL = 'signin'
LOGIN_REDIRECT_URL = 'index'
LOGOUT_REDIRECT_URL = 'signin'

"""

authconf = """
    
CRISPY_TEMPLATE_PACK = 'bootstrap4'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'accounts.authentication.EmailOrUsernameModelBackend',
)

"""


def wrtingSettingsFile(corePath:str, auth:bool) -> bool:
    try:
        with open(os.path.join(corePath, 'settings.py'), 'r') as settingsf:
            settingsread = settingsf.readlines()
        settingsread[27] = "ALLOWED_HOSTS = ['*']"
        settingsread[38] = "\n\t# Apps\n\t'app.apps.AppConfig',\n\n\t# Third party apps\n\n"
        settingsread[48] = "\t'whitenoise.middleware.WhiteNoiseMiddleware',\n"
        settingsread[56] = "\t\t'DIRS': ['templates'],\n"
        settingsread[114:-1] = confSettings
        if auth:
            settingsread[38] = "\n\t# Apps\n\t'app.apps.AppConfig',\n\n\t# Third party apps\n\t'accounts',\n\t'crispy_forms',\n\n"
            settingsread[114:-1] = confSettings + authconf
        print("Finalyzing And Writting The settings.py File.")
        with open(os.path.join(corePath, 'settings.py'), 'w') as settingsw:
            settingsw.writelines(settingsread)
        return True
    except Exception as err:
        print('Settings Error: ', err)
        return False
