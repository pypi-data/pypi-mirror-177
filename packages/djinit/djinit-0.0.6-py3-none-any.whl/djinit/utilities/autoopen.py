import os

def autoOpen(projectPath:str) -> bool:
    try:
        with open(os.path.join(projectPath, 'browser.py'), 'w') as browserbatch:
            browserbatch.write("import webbrowser\nimport os\nenvPath = os.path.join(os.getcwd(), 'env/Scripts/activate')\n\nwebUrl = 'http://127.0.0.1:8000'\nchrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s --incognito'\n\nwebbrowser.get(chrome_path).open_new(webUrl)\nos.system(f'{envPath} & python manage.py runserver --skip-checks')\n")
        return True
    except Exception as err:
        print('AutoOpen Error: ', err.__class__.__name__)
        return False
