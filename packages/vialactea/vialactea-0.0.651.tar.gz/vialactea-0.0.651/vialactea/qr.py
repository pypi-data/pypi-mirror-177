# Sirius Tech. Studio, 2022
import qrcode
import os
import qrcode.image.svg
from datetime import datetime
from vialactea.sirius import QR_DEFAULT_IMPORTSRC

class siriusqr(qrcode.QRCode):

    _IMPORT_SRC_ = QR_DEFAULT_IMPORTSRC
    _EXPORT_SRC_ = 'downloads\\siriusqr\\'
    _IMG_TYPE_FACTORY_ = qrcode.image.svg.SvgImage
    _IMG_TYPE_EXTENSION = 'svg'

    def __init__(self):
        super().__init__()

        self.import_src = os.path.join(os.path.dirname(__file__), self._IMPORT_SRC_)
        self.export_src = os.path.join(os.path.expanduser('~'), self._EXPORT_SRC_)
        self.version = 4
        self.error_correction = qrcode.constants.ERROR_CORRECT_M
        self.box_size = 50
        self.border = 3
        self.current_data = ''

        if os.path.isdir(self.export_src):
            pass
        else:
            os.makedirs(self.export_src)

    def set_version(self, version_value):

        if isinstance(version_value, int):
            if version_value >= 1 <= 44:
                self.version = version_value
            else:
                self.version = 4
                print(
                    'You tried to set an version param that is out of its bounds.\nYou should try an integer value between 1 till 44.\nLimit was set to application default (4)')
        elif isinstance(version_value, float):
            if int(version_value) >= 1 <= 44:
                self.version = int(version_value)
                print('Float type was catch in pixels param and should not be used.\npixels param was applied using int method')
            else:
                self.version = 4
                print(
                    'You tried to set an version param that is out of its bounds.\nYou should try an integer value between 1 till 44.\nLimit was set to application default (4)')
        else:
            self.version = 4
            print(
                'You tried to set an non-numeric argument.\nYou should try an integer value between 1 till 44.\nLimit was set to application default (4)')

    def get_version(self):
        return self.version

    def set_error_c(self, acc_lvl: str):
        """
        Accuracy error treatment  you can set low, medium, quarter or high if anything different from the known arguments is passed, bifrost will set medium acc_error lvl as default
        :param acc_lvl:
        :return:
        """
        match acc_lvl:
            case 'low':
                self.error_correction = qrcode.constants.ERROR_CORRECT_L
            case 'medium':
                self.error_correction = qrcode.constants.ERROR_CORRECT_M
            case 'quarter':
                self.error_correction = qrcode.constants.ERROR_CORRECT_Q
            case 'high':
                self.error_correction = qrcode.constants.ERROR_CORRECT_H
            case _:
                self.error_correction = qrcode.constants.ERROR_CORRECT_M
                raise KeyError('The argument for accuracy error does not match with any option supported.\n In that case, error accuracy was set to medium (default) level')

    def get_error_c(self):
        return self.error_correction

    def set_box_size(self, pixels=10):
        """
        The box_size parameter controls how many pixels each “box” of the QR code is
        :param pixels:
        :return:
        """
        if isinstance(pixels, int):
            self.box_size = pixels
        elif isinstance(pixels, float):
            self.box_size = int(pixels)
            raise Warning('Float type was catch in pixels param and should not be used.\npixels param was applied using int method')
        else:
            self.box_size = 10
            raise TypeError(f'Bifrost could not apply {pixels} value because is not an numeric type. Box_size was set do default value (10)')

    def get_box_size(self):
        return self.box_size

    def set_border(self, boxes):
        box_warning = 'Boxes default is 4, according to specs.\nYou should work with that value'
        if isinstance(boxes, int):
            self.border = boxes
            raise Warning(box_warning)
        elif isinstance(boxes, float):
            self.border = int(boxes)
            print(
                'Float type was catch in pixels param and should not be used.\npixels param was applied using int method')
            raise Warning(box_warning)
        else:
            self.border = 4
            raise TypeError(
                f'Bifrost could not apply {boxes} value because is not an numeric type. border was set do default value (4)')

    def get_border(self):
        return self.border

    def read_import(self):
        return open(self.import_src, 'r').readlines()

    def set_data(self, text_value: str):
        self.current_data = text_value
        self.add_data(text_value)

    def reset_data(self):
        self.clear()
        self.current_data = ''

    def create(self):
        """Create an QR Code according to current_data content"""
        img = self.make_image(image_factory=self._IMG_TYPE_FACTORY_)
        if self.current_data == '' or None:
            self.current_data = str(datetime.now().strftime('%d%m%Y%I%M%S%p'))
        img.save(f'{self.export_src}{self.current_data}.{self._IMG_TYPE_EXTENSION}')

    def set_importsrc(self, path_to_importsrc):
        if os.path.isfile(path_to_importsrc):
            if path_to_importsrc.lower().endswith('.txt'):
                self.import_src = path_to_importsrc
            else:
                self.import_src = os.path.join(os.path.dirname(__file__), self._IMPORT_SRC_)
                raise TypeError('File could not be readed')

    def create_from_import(self):
        lines = self.read_import()

        for line in lines:
            self.set_data(text_value=line.rstrip())
            img = self.make_image(image_factory=self._IMG_TYPE_FACTORY_)

            if self.current_data == '' or None:
                self.current_data = str(datetime.now().strftime('%d%m%Y%I%M%S%p'))
            img.save(f'{self.export_src}{self.current_data.replace(".","").replace("/","").replace("=","").replace(":","").replace("?","").replace("_","")}{self.get_version()}V.{self._IMG_TYPE_EXTENSION}')
            self.reset_data()
