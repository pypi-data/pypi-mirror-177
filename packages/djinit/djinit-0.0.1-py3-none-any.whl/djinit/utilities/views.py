import os


def wrtingViewsFile(appPath:str,) -> bool:
    try:
        viewContent = (f"from django.shortcuts import render\n")
        with open(os.path.join(appPath, 'views.py'), 'w') as vieww:
            vieww.write(viewContent)
        return True
    except Exception as err:
        print('Views Error: ', err.__class__.__name__)
        return False
