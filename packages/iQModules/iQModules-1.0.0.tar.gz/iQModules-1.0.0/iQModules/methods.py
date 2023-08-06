# ----------------------------------------------------------------------------
# Description:  iQModules (модуль методов)
#
# Project  : iQModules (https://gitflic.ru/project/iqstudio/iqmodules)
# Date     : 19.11.2022
# Author   : KhAN (Alexander Khilchenko)
#               khan.programming@mail.ru, github.com/nikodim-an
# License  : MIT
# ----------------------------------------------------------------------------

def get_time_stamp() -> str:
    """ Отметка времени формата дд.мм.гггг-чч:мм:сс"""
    import datetime
    now = datetime.datetime.now()
    return f"{now.day}.{now.month}.{now.year}" \
           f"-{now.hour}:{now.minute}:{now.second}"


def get_desktop_path():
    """ Путь к папке рабочего стола linux средствами xdg"""
    import subprocess
    try:
        return subprocess.check_output(['xdg-user-dir', 'DESKTOP']).\
            decode('utf-8').replace('\n', '')
    except BaseException:
        raise BaseException('На ПК XDG')


def get_pictures_path():
    """ Путь к папке картинок linux средствами xdg"""
    import subprocess
    try:
        return subprocess.check_output(['xdg-user-dir', 'PICTURES']).\
            decode('utf-8').replace('\n', '')
    except BaseException:
        raise BaseException('На ПК нет XDG')


def get_templates_path():
    """ Путь к папке шаблонов документов linux средствами xdg"""
    import subprocess
    try:
        return subprocess.check_output(['xdg-user-dir', 'TEMPLATES']).\
            decode('utf-8').replace('\n', '')
    except BaseException:
        raise BaseException('На ПК нет XDG')


def get_public_path():
    """ Путь к папке общедоступных linux средствами xdg"""
    import subprocess
    try:
        return subprocess.check_output(['xdg-user-dir', 'PUBLICSHARE']).\
            decode('utf-8').replace('\n', '')
    except BaseException:
        raise BaseException('На ПК нет XDG')


def get_music_path():
    """ Путь к папке музыки linux средствами xdg"""
    import subprocess
    try:
        return subprocess.check_output(['xdg-user-dir', 'MUSIC']).\
            decode('utf-8').replace('\n', '')
    except BaseException:
        raise BaseException('На ПК нет XDG')


def get_videos_path():
    """ Путь к папке видео linux средствами xdg"""
    import subprocess
    try:
        return subprocess.check_output(['xdg-user-dir', 'VIDEOS']).\
            decode('utf-8').replace('\n', '')
    except BaseException:
        raise BaseException('На ПК нет XDG')


def get_download_path():
    """ Путь к папке загрузок linux средствами xdg"""
    import subprocess
    try:
        return subprocess.check_output(['xdg-user-dir', 'DOWNLOAD']).\
            decode('utf-8').replace('\n', '')
    except BaseException:
        raise BaseException('На ПК нет XDG')


def get_documents_path():
    """ Путь к папке документов linux средствами xdg"""
    import subprocess
    try:
        return subprocess.check_output(['xdg-user-dir', 'DOCUMENTS']).\
            decode('utf-8').replace('\n', '')
    except BaseException:
        raise BaseException('На ПК нет XDG')



