import os
import shutil
import djinit
from .utilities import (
    project, settings,
    views, urls,
    autoopen,
)


def main():
    modpath = os.path.dirname(djinit.__file__)
    mainPath:str = os.getcwd()
    os.chdir(mainPath)

    try:
        # projectName:str =  'Task'.lower()
        projectName:str =  input('Enter your project folder name (Case-In-Sensitive): ').lower()
        if projectName == 'test': raise NameError
        if os.path.exists(projectName): raise NameError
    except NameError as err:
        print('Error: ', err.__class__.__name__)
        exit()


    projectPath = os.path.join(mainPath, projectName)
    envPath = os.path.join(projectPath, 'env/Scripts/activate')
    ####### Starting Project... ###################
    project.startDjangoProject(envPath, projectName)
    ####### Ending Project! #######################

    corePath = os.path.join(projectName, 'core')
    appPath = os.path.join(projectName, 'app')

    ####### Copying Project Files... ##############
    curTempPath = os.path.join(modpath, 'utilities/templates')
    projTempPath = os.path.join(projectPath, 'templates')
    shutil.copytree(curTempPath, projTempPath)
    with open(os.path.join(corePath, 'static/css/style.css'), 'w') as f: f.write('')
    with open(os.path.join(corePath, 'static/js/script.js'), 'w') as f: f.write('')
    ####### Copied! ###############################

    ####### Modifying settings... ###############
    settings.wrtingSettingsFile(corePath)
    ####### Ending settings modifications! ########

    ####### Modifying views... ##################
    views.wrtingViewsFile(appPath)
    ####### Ending views modifications! ###########

    ####### Modifying urls... ###################
    urls.wrtingUrlsFile(corePath, appPath)
    ####### Ending urls modifications! ############

    ####### Writing auto open python file... #####
    autoopen.autoOpen(projectPath)
    ####### Auto open file writing completed! #####

    print('Starting...')
    ####### Calling browser file... #############
    os.system(f'cd {projectPath} & python browser.py')
    ####### End! ######
    print('Done!')


if __name__ == 'main':
    main()
