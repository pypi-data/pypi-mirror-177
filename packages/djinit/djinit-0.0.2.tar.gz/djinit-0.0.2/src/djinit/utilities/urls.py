import os


def wrtingUrlsFile(corePath:str, appPath:str) -> bool:
    try:
        finalstrforurlscore = (f"from django.contrib import admin\nfrom django.urls import path, include\nfrom django.conf import settings\nfrom django.conf.urls.static import static\n\nurlpatterns = [\n\tpath('admin/', admin.site.urls),\n\tpath('', include('app.urls')),\n] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)\n")
        finalstrforurlapp = (f"from django.urls import path\nfrom . import views\n\nurlpatterns = [\n\tpath('', views.index, name='index'),\n]\n")

        with open(os.path.join(corePath, 'urls.py'), 'w') as urlf:
            urlf.writelines(finalstrforurlscore)

        with open(os.path.join(appPath, 'urls.py'), 'w') as urlw:
            urlw.writelines(finalstrforurlapp)

        return True
    except Exception as err:
        print('Urls Error: ', err.__class__.__name__)
        return False
