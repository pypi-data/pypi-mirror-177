import os


def wrtingViewsFile(appPath:str,) -> bool:
    try:
        viewContent = "from django.shortcuts import render\n\n\ndef index(request):\n\tcontext = {\n\t\t'': ''\n\t}\n\treturn render(request, 'index.html', context)"
        with open(os.path.join(appPath, 'views.py'), 'w') as vieww:
            vieww.writelines(viewContent)
        return True
    except Exception as err:
        print('Views Error: ', err.__class__.__name__)
        return False
