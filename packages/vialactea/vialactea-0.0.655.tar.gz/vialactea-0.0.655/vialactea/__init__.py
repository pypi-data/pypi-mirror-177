# Sirius Tech. Studio, 2022
import os, winshell, shutil

from vialactea.sirius import report, Studio
from vialactea.bifrost import _bifrost


for dir in _bifrost.PERSIST_DIRECTORIES:
        if os.path.exists(dir):
            pass
        else:
            os.makedirs(dir)

for link in _bifrost.NAV_DIR_LINKS:
        with winshell.shortcut(link) as flink:
            flink.path = link
            flink.description = link.split('\\')[-1]

for file in list(os.listdir(_bifrost.vialactea_in_dir)):
        if '.lnk' in file:
            shutil.move(f'{_bifrost.vialactea_in_dir}\\{file}', f'{_bifrost.nav_dir}\\{file}')