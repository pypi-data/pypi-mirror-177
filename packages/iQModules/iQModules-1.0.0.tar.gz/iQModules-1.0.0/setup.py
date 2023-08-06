import setuptools

read_me_description = """
# Библиотека поддержки проектов iQStudio
## Состав
 - класс поддержки работы с настройками программы
 - временной штамп
 - методы возвращающие стандартные пути окружений из xdg (рабочий стол, картинки, документы, загрузки, …)

## Примеры
Включены в репозиторий.

## Лицензия
MIT

## Подробности
подробности на https://gitflic.ru/project/iqstudio/iqmodules
"""


setuptools.setup(
    name="iQModules",
    version="1.0.0",
    author="Alexander N Khilchenko",
    author_email="khan.programming@mail.ru",
    description="iQModules (библиотека поддержки проектов iQStudio)",
    long_description=read_me_description,
    long_description_content_type="text/markdown",
    url="https://gitflic.ru/project/iqstudio/iqmodules",
    packages=['iQModules'],
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: Russian",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Environment :: X11 Applications :: Qt",
        "Topic :: Desktop Environment",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
        "Typing :: Typed",
    ],
    python_requires='>=3.6',
)

