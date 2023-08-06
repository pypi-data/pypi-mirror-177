import json
from pathlib import Path

# ----------------------------------------------------------------------------
# Description: Модуль с классами библиотеки iQModules
#
# Project : iQModules (https://gitflic.ru/project/iqstudio/iqmodules)
# Date    : 19.11.2022
# Author  : KhAN (Alexander Khilchenko)
#           khan.programming@mail.ru, github.com/nikodim-an
# ----------------------------------------------------------------------------


class Settings:
    """
    Класс сохраняющий настройки в ~/config
    """
    __options = {}

    # Конструктор
    def __init__(self, app_name: str, **kwargs):
        """
            При создании обязательно передавать app_name!
            Параметры по умолчанию передаются в options={…}
            Созданный экземпляр сразу формирует структуру каталогов и файлов
            для хранения настроек.
        """
        self.__app_name = app_name
        self.__settings_folder = Path().home() / Path(".config") / Path(
            app_name)
        self.__settings_file = self.__settings_folder / Path('.rc')
        if ('options' in kwargs) and (isinstance(kwargs['options'], dict)):
            self.__options = kwargs['options']
        # загрузка после инициализации
        if self.__settings_folder.exists():
            self.load()
        else:
            self.__settings_folder.mkdir(
                parents=True,
                exist_ok=False)

    # представление для логгера
    def __str__(self):
        def get_options():
            res = ""
            for i in self.__options:
                res += f'\t\t{i}: {self.__options[i]}\n'
            return res

        return f"Текущие настройки:\n\t{self.__settings_folder}" \
               f"\n{get_options()}"

    # геттеры и сеттеры
    @property
    def options(self):
        return self.__options

    @options.setter
    def options(self, value):
        self.__options = value

    @property
    def settings_folder(self):
        return self.__settings_folder

    @property
    def settings_file(self):
        return self.__settings_file

    @property
    def app_name(self):
        return self.__app_name

    # сохранение и восстановление
    def save(self):
        with open(self.__settings_file, 'w', encoding='utf-8') as f:
            json.dump(self.__options, f, indent=4, ensure_ascii=False)

    def load(self):
        try:
            if self.__settings_file.exists():
                with open(self.__settings_file) as f:
                    self.__options = json.load(f)
        except BaseException:
            raise BaseException(
                'Ошибка чтения файла настроек (файл настроек поврежден)'
            )
