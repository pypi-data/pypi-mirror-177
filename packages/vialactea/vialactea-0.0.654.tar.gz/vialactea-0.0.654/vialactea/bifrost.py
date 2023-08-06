import os
import winshell
import shutil


class Bifrost:
    c_user = os.environ['userprofile']
    local_appdata = os.environ['localappdata']
    tmp = os.environ['tmp']
    desktop = winshell.desktop()
    vialactea_in_dir = os.path.dirname(__file__)

    vialactea_dir = os.path.join(local_appdata, 'vialactea')
    vialactea_import = os.path.join(vialactea_dir, 'import')
    vialactea_export = os.path.join(vialactea_dir, 'export')
    vialactea_log = os.path.join(vialactea_dir, 'log')

    nav_dir = os.path.join(desktop, 'ViaLactea Navigation')

    PERSIST_DIRECTORIES = [
        nav_dir,
        vialactea_dir,
        vialactea_import,
        vialactea_export,
        vialactea_log
    ]

    NAV_DIR_LINKS = [
        vialactea_dir,
        vialactea_import,
        vialactea_export,
        vialactea_log
    ]

    for dir in PERSIST_DIRECTORIES:
        if os.path.exists(dir):
            pass
        else:
            os.makedirs(dir)

    for link in NAV_DIR_LINKS:
        with winshell.shortcut(link) as flink:
            flink.path = link
            flink.description = link.split('\\')[-1]

    for file in list(os.listdir(vialactea_in_dir)):
        if '.lnk' in file:
            shutil.move(f'{vialactea_in_dir}\\{file}', f'{nav_dir}\\{file}')


_bifrost = Bifrost()
