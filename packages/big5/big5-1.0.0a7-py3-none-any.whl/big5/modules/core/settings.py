#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Настройки
"""

# ######################################################################################################################
# Импорт необходимых инструментов
# ######################################################################################################################
# Подавление Warning
import warnings
for warn in [UserWarning, FutureWarning]: warnings.filterwarnings('ignore', category = warn)

from dataclasses import dataclass # Класс данных

import os # Взаимодействие с файловой системой
import re # Регулярные выражения

from typing import List

# Персональные
from big5.modules.core.messages import Messages # Сообщения

# ######################################################################################################################
# Настройки
# ######################################################################################################################
@dataclass
class Settings(Messages):
    """Класс для настроек

    Args:
        lang (str): Смотреть :attr:`~big5.modules.core.language.Language.lang`
        color_simple (str): Цвет обычного текста (шестнадцатеричный код)
        color_info (str): Цвет текста содержащего информацию (шестнадцатеричный код)
        color_err (str): Цвет текста содержащего ошибку (шестнадцатеричный код)
        bold_text (bool): Жирное начертание текста
        text_runtime (str): Текст времени выполнения
    """

    # ------------------------------------------------------------------------------------------------------------------
    # Конструктор
    # ------------------------------------------------------------------------------------------------------------------

    # Цвет текстов
    color_simple: str = '#666'
    """
    str: Цвет обычного текста (шестнадцатеричный код)
    """

    color_info: str = '#1776D2'
    """
    str: Цвет текста содержащего информацию (шестнадцатеричный код)
    """

    color_err: str = '#FF0000'
    """
    str: Цвет текста содержащего ошибку (шестнадцатеричный код)
    """

    bold_text: bool = True
    """
    bool: Жирное начертание текста
    """

    text_runtime: str = ''
    """
    str: Текст времени выполнения
    """

    num_to_df_display: int = 0
    """
    int: Количество строк для отображения в таблицах
    """

    def __post_init__(self):
        super().__post_init__() # Выполнение конструктора из суперкласса

        self.__re_search_color: str = r'^#(?:[0-9a-fA-F]{3}){1,2}$' # Регулярное выражение для корректности ввода цвета

        # Цвет текстов
        self.__color_simple_true: int = 0 # Счетчик изменения текста
        self.color_simple_: str = self.color_simple # Обычный текст

        self.__color_info_true: int = 0  # Счетчик изменения текста
        self.color_info_: str = self.color_info # Цвет текста содержащего информацию

        self.__color_err_true: int = 0 # Счетчик изменения текста
        self.color_err_: str = self.color_err # Цвет текста содержащего ошибку

        self.bold_text_: bool = self.bold_text # Жирное начертание текста

        self.__text_runtime_true: int = 0 # Счетчик изменения текста
        self.text_runtime_: str = self.text_runtime # Текст времени выполнения

        # Количество строк для отображения в таблицах
        self.num_to_df_display_: int = 30
        self.num_to_df_display_ = self.num_to_df_display

        self.chunk_size_: int = 1000000 # Размер загрузки файла из сети за 1 шаг (1 Mb)

        self.path_to_save_: str = './models' # Директория для сохранения данных

        self.path_to_dataset_: str = '' # Директория набора данных
        self.ext_: List[str] = [] # Расширения искомых файлов
        self.ignore_dirs_: List[str] = [] # Директории не входящие в выборку
        # Названия ключей для DataFrame набора данных
        self.keys_dataset_: List[str] = [
            'Path', 'Openness', 'Conscientiousness', 'Extraversion', 'Agreeableness', 'Neuroticism'
        ]

    # ------------------------------------------------------------------------------------------------------------------
    # Свойства
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def color_simple_(self) -> str:
        """Получение/установка цвета обычного текста

        Args:
            (str): Шестнадцатеричный код

        Returns:
            str: Шестнадцатеричный код

        Example:
            .. code-cell:: python
                :execution-count: 1
                :linenos:

                from big5.modules.core.settings import Settings

                settings = Settings(color_simple = '#111')
                print(settings.color_simple_)

                settings.color_simple_ = '#777'
                print(settings.color_simple_)

            .. output-cell::
                :execution-count: 1
                :linenos:

                #111
                #777
        """

        return self.color_simple

    @color_simple_.setter
    def color_simple_(self, color: str) -> None:
        """Установка цвета обычного текста"""

        match = re.search(self.__re_search_color, color)

        try:
            # Проверка аргументов
            if not match: raise TypeError
        except TypeError:
            if self.__color_simple_true == 0:
                self.color_simple = '#666'
        else:
            self.color_simple = color
            self.__color_simple_true += 1 # Увеличение счетчика изменения цвета текста

    @property
    def color_info_(self) -> str:
        """Получение/установка цвета текста содержащего информацию

        Args:
            (str): Шестнадцатеричный код

        Returns:
            str: Шестнадцатеричный код

        Example:
            .. code-cell:: python
                :execution-count: 1
                :linenos:

                from big5.modules.core.settings import Settings

                settings = Settings(color_info = '#999')
                print(settings.color_info_)

                settings.color_info_ = '#888'
                print(settings.color_info_)

            .. output-cell::
                :execution-count: 1
                :linenos:

                #999
                #888
        """

        return self.color_info

    @color_info_.setter
    def color_info_(self, color: str) -> None:
        """Установка цвета текста содержащего информацию"""

        match = re.search(self.__re_search_color, color)

        try:
            # Проверка аргументов
            if not match: raise TypeError
        except TypeError:
            if self.__color_info_true == 0:
                self.color_info = '#1776D2'
        else:
            self.color_info = color
            self.__color_info_true += 1 # Увеличение счетчика изменения цвета текста

    @property
    def color_err_(self) -> str:
        """Получение/установка цвета текста содержащего ошибку

        Args:
            (str): Шестнадцатеричный код

        Returns:
            str: Шестнадцатеричный код

        Example:
            .. code-cell:: python
                :execution-count: 1
                :linenos:

                from big5.modules.core.settings import Settings

                settings = Settings(color_err = '#C22931')
                print(settings.color_err_)

                settings.color_err_ = '#C229F1'
                print(settings.color_err_)

            .. output-cell::
                :execution-count: 1
                :linenos:

                #C22931
                #C229F1
        """

        return self.color_err

    @color_err_.setter
    def color_err_(self, color: str) -> None:
        """Установка цвета текста содержащего ошибку"""

        match = re.search(self.__re_search_color, color)

        try:
            # Проверка аргументов
            if not match: raise TypeError
        except TypeError:
            if self.__color_err_true == 0:
                self.color_err = '#FF0000'
        else:
            self.color_err = color
            self.__color_err_true += 1 # Увеличение счетчика изменения цвета текста

    @property
    def bold_text_(self) -> bool:
        """Получение/установка жирного начертания текста

        Args:
            (bool): **True** или **False**

        Returns:
            bool: **True** или **False**

        Example:
            .. code-cell:: python
                :execution-count: 1
                :linenos:

                from big5.modules.core.settings import Settings

                settings = Settings(bold_text = False)
                print(settings.bold_text_)

                settings.bold_text_ = True
                print(settings.bold_text_)

            .. output-cell::
                :execution-count: 1
                :linenos:

                False
                True
        """

        return self.bold_text

    @bold_text_.setter
    def bold_text_(self, bold: bool) -> None:
        """Установка жирного начертания текста"""

        self.bold_text = bold

    @property
    def text_runtime_(self) -> str:
        """Получение/установка текста времени выполнения

        Args:
            (str): Текст

        Returns:
            str: Текст

        Example:
            .. code-cell:: python
                :execution-count: 1
                :linenos:

                from big5.modules.core.settings import Settings

                settings = Settings(text_runtime = 'Время выполнения')
                print(settings.text_runtime_)

                settings.text_runtime_ = 'Код выполнился за'
                print(settings.text_runtime_)

            .. output-cell::
                :execution-count: 1
                :linenos:

                'Время выполнения'
                'Код выполнился за'
        """

        return self.text_runtime

    @text_runtime_.setter
    def text_runtime_(self, text: str) -> None:
        """Установка текста времени выполнения"""

        try:
            # Проверка аргументов
            if type(text) is not str or len(text) < 1: raise TypeError
        except TypeError:
            if self.__text_runtime_true == 0:
                self.text_runtime = self._text_runtime
        else:
            self.text_runtime = text
            self.__text_runtime_true += 1 # Увеличение счетчика изменения текста времени выполнения

    @property
    def num_to_df_display_(self) -> int:
        """Получение/установка количества строк для отображения в таблицах

        Args:
            (int): Количество строк

        Returns:
            int: Количество строк

        Example:
            .. code-cell:: python
                :execution-count: 1
                :linenos:

                from big5.modules.core.settings import Settings

                settings = Settings(num_to_df_display = 10)
                print(settings.text_runtime_)

                settings.num_to_df_display_ = 5
                print(settings.num_to_df_display_)

            .. output-cell::
                :execution-count: 1
                :linenos:

                10
                5
        """

        return self._num_to_df_display

    # Установка количества строк для отображения в таблицах
    @num_to_df_display_.setter
    def num_to_df_display_(self, num: int) -> None:
        """Установка количества строк для отображения в таблицах"""

        if type(num) is not int or num < 1 or num > 50: return self._num_to_df_display
        self._num_to_df_display = num

    @property
    def path_to_save_(self) -> str:
        """Получение/установка директории для сохранения данных

        Args:
            (str): Директория для сохранения данных

        Returns:
            str: Директория для сохранения данных

        Example:
            .. code-cell:: python
                :execution-count: 1
                :linenos:

                from big5.modules.core.settings import Settings

                settings = Settings()
                print(settings.path_to_save_)

                settings.path_to_save_ = './models/Audio'
                print(settings.path_to_save_)

            .. output-cell::
                :execution-count: 1
                :linenos:

                './models'
                './models/Audio'
        """

        return self._path_to_save

    @path_to_save_.setter
    def path_to_save_(self, path: str) -> None:
        """Установка директории для сохранения данных"""

        if type(path) is str and len(path) > 0: self._path_to_save = os.path.normpath(path)

    @property
    def chunk_size_(self) -> int:
        """Получение/установка размера загрузки файла из сети за 1 шаг

        Args:
            (int): Размер загрузки файла из сети за 1 шаг

        Returns:
            int: Размер загрузки файла из сети за 1 шаг

        Example:
            .. code-cell:: python
                :execution-count: 1
                :linenos:

                from big5.modules.core.settings import Settings

                settings = Settings()
                print(settings.chunk_size_)

                settings.chunk_size_ = 2000000
                print(settings.chunk_size_)

            .. output-cell::
                :execution-count: 1
                :linenos:

                1000000
                2000000
        """

        return self._chunk_size

    @chunk_size_.setter
    def chunk_size_(self, size: int) -> None:
        """Установка директории для сохранения данных"""

        if type(size) is int and size > 0: self._chunk_size = size

    @property
    def path_to_dataset_(self) -> str:
        """Получение/установка директории набора данных

        Args:
            (str): Директория набора данных

        Returns:
            str: Директория набора данных

        Example:
            .. code-cell:: python
                :execution-count: 1
                :linenos:

                from big5.modules.core.settings import Settings

                settings = Settings()
                print(settings.path_to_dataset_)

                settings.path_to_dataset_ = './dataset'
                print(settings.path_to_dataset_)

            .. output-cell::
                :execution-count: 1
                :linenos:

                ''
                './dataset'
        """

        return self._path_to_dataset

    @path_to_dataset_.setter
    def path_to_dataset_(self, path: str) -> None:
        """Установка директории набора данных"""

        self._path_to_dataset = os.path.normpath(path)

    @property
    def keys_dataset_(self):
        """Получение/установка названий ключей набора данных

        Args:
            (List[str]): Список с названиями ключей набора данных

        Returns:
            List[str]: Список с названиями ключей набора данных

        Example:
            .. code-cell:: python
                :execution-count: 1
                :linenos:

                from big5.modules.core.settings import Settings

                settings = Settings()
                print(settings.keys_dataset_)

                settings.keys_dataset_ = ['P', 'O', 'C', 'E', 'A', 'N']
                print(settings.keys_dataset_)

            .. output-cell::
                :execution-count: 1
                :linenos:

                ['Path', 'Openness', 'Conscientiousness', 'Extraversion', 'Agreeableness', 'Neuroticism']
                ['P', 'O', 'C', 'E', 'A', 'N']
        """

        return self._keys_dataset

    # Установка названий ключей набора данных
    @keys_dataset_.setter
    def keys_dataset_(self, keys: List[str]) -> None:
        """Установка названий ключей набора данных"""

        if type(keys) is not list or len(keys) != 6: self._keys_dataset = [
            'Path', 'Openness', 'Conscientiousness', 'Extraversion', 'Agreeableness', 'Neuroticism'
        ]
        else: self._keys_dataset = keys

    @property
    def ignore_dirs_(self) -> List[str]:
        """Получение/установка списка с директориями не входящими в выборку

        Args:
            (List[str]): Список с директориями

        Returns:
            List[str]: Список с директориями

        Example:
            .. code-cell:: python
                :execution-count: 1
                :linenos:

                from big5.modules.core.settings import Settings

                settings = Settings()
                print(settings.ignore_dirs_)

                settings.ignore_dirs_ = ['test', 'test_2']
                print(settings.ignore_dirs_)

            .. output-cell::
                :execution-count: 1
                :linenos:

                []
                ['test', 'test_2']
        """

        return self._ignore_dirs

    @ignore_dirs_.setter
    def ignore_dirs_(self, l: List[str]) -> None:
        """Установка списка с директориями не входящими в выборку"""

        if type(l) is not list: self._ignore_dirs = []
        else: self._ignore_dirs = l

    @property
    def ext_(self) -> List[str]:
        """Получение/установка расширений искомых файлов

        Args:
            (List[str]): Список с расширениями искомых файлов

        Returns:
            List[str]: Список с расширениями искомых файлов

        Example:
            .. code-cell:: python
                :execution-count: 1
                :linenos:

                from big5.modules.core.settings import Settings

                settings = Settings()
                print(settings.ext_)

                settings.ext_ = ['.mp4']
                print(settings.ext_)

            .. output-cell::
                :execution-count: 1
                :linenos:

                []
                ['.mp4']
        """

        return self._ext

    @ext_.setter
    def ext_(self, ext: List[str]):
        """Установка расширений искомых файлов"""

        self._ext = ext