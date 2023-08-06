import json
import os
from datetime import datetime
import math
import time
import pandas as pd
from vialactea.feed import Notifications
from vialactea.bifrost import _bifrost


notif = Notifications()

def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


class report:
    def __init__(self):
        self._path = os.path.join(_bifrost.vialactea_log,'log.txt')

        if os.path.exists(self._path):
            pass
        else:
            with open(self._path, 'w', encoding='utf-8') as f:
                f.write('Sirius Tech. Studio, 2022\n')
                f.write(f'{"="*100}\n')
                f.write(f'[{datetime.now():%d/%m/%Y %H:%M:%S}];NOTIFICATION;Log file created\n')
        with open(self._path, 'r', encoding='utf-8') as f:
            self.file = f.read()

    def reload(self):
        with open(self._path, 'w', encoding='utf-8') as f:
            f.write(self.file)
        with open(self._path, 'r', encoding='utf-8') as f:
            self.file = f.read()

    def set_value(self, text):
        self.file += f'{"=" * 100}\n'
        self.file += f'[{datetime.now():%d/%m/%Y %H:%M:%S}];{text}\n'
        self.reload()

    @staticmethod
    def describe_dir(target_dir):
        """
        Generates report with Name, Date, Type and Size
        :param target_dir:
        :return:
        """
        report_headers = ['File Name', 'Last Date Modified', 'Extension', 'Size']
        report_content = []
        file__name_tosave = ''.join(
            [
                _bifrost.vialactea_export,
                target_dir.split('/')[-2].upper(),
                '_DESCRIPTION_REPORT.csv'
            ]
        )

        if os.path.isdir(target_dir):
            list_dir = os.listdir(target_dir)

            for file in list_dir:
                file_path = f'{target_dir}/{file}'
                _ = list()
                _.append(file)
                _.append(time.strftime("%Y-%m-%d %H:%M:%S", time.strptime(time.ctime(os.path.getctime(file_path)))))
                _.append(file.split('.')[-1])
                _.append(convert_size(os.path.getsize(file_path)))
                report_content.append(_)

            df = pd.DataFrame(data=report_content, columns=report_headers)
            df.to_csv(file__name_tosave, index=False, sep=';')


class bifrost:
    def __init__(self):
        self._path = _bifrost.vialactea_dir

    class tools:

        def __init__(self):
            pass

        @staticmethod
        def validate_path(target_dir):

            if os.path.isdir(target_dir):
                return {'type': 'dir', 'content': target_dir}
            elif os.path.isfile(target_dir):
                return {'type': 'file', 'content': target_dir}
            else:
                return {'type': 'unknown', 'content': target_dir}

        def dir_handler(self, target_dir):
            if self.validate_path(target_dir)['type'] == 'dir':
                return {'type': 'handler', 'path': target_dir, 'content': os.listdir(target_dir)}
            else:
                print(f'Error {target_dir} is not a dir.')


        @staticmethod
        def list_textfilter(target_list: list, inFilter=' ', outFilter=' '):
            """
            Filter a list using in and out arguments.
            inFilter is for include the param
            outFilter is when you want to exclude the param from the current list
            IMPORTANT! This does not cover all regex structures
            :param target_list:
            :param inFilter:
            :param outFilter:
            :return:
            """
            # todo COLOCAR O UPPER E CHECAR DE FOI PASSADO ''
            
            print(notif.FUNC_UNDER_MAINTENANCE)

            out_target_list = []
            in_target_list = []

            for out_list_item in target_list:
                if outFilter in out_list_item:
                    pass
                else:
                    out_target_list.append(out_list_item)

            for _list_item in out_target_list:
                if inFilter in _list_item:
                    in_target_list.append(_list_item)
                else:
                    pass

            return in_target_list
