#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Ядро
"""

# ######################################################################################################################
# Импорт необходимых инструментов
# ######################################################################################################################
# Подавление Warning
import warnings
for warn in [UserWarning, FutureWarning]: warnings.filterwarnings('ignore', category = warn)

from dataclasses import dataclass # Класс данных

import os                 # Взаимодействие с файловой системой
import sys                # Доступ к некоторым переменным и функциям Python
import re                 # Регулярные выражения
import time               # Работа со временем
import numpy as np        # Научные вычисления
import pandas as pd       # Обработка и анализ данных
import opensmile          # Анализ, обработка и классификация звука
import jupyterlab as jlab # Интерактивная среда разработки для работы с блокнотами, кодом и данными
import requests           # Отправка HTTP запросов
import librosa            # Обработка аудио
import audioread          # Декодирование звука
import sklearn            # Машинное обучение и интеллектуальный анализ данных
import IPython
import logging

from datetime import datetime # Работа со временем
from typing import List, Dict, Tuple, Union, Iterable # Типы данных

from IPython import get_ipython
from IPython.display import Markdown, display

# Персональные
import big5                                     # big5 - персональные качества личности человека
from big5.modules.core.settings import Settings # Глобальный файл настроек

# Порог регистрации сообщений TensorFlow
logging.disable(logging.WARNING)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import tensorflow as tf # Машинное обучение от Google
import keras

# ######################################################################################################################
# Сообщения
# ######################################################################################################################
@dataclass
class CoreMessages(Settings):
    """Класс для сообщений

    Args:
        lang (str): смотреть :attr:`~big5.modules.core.language.Language.lang`
        color_simple (str): смотреть :attr:`~big5.modules.core.settings.Settings.color_simple`
        color_info (str): Смотреть :attr:`~big5.modules.core.settings.Settings.color_info`
        color_err (str): Смотреть :attr:`~big5.modules.core.settings.Settings.color_err`
        bold_text (bool): Смотреть :attr:`~big5.modules.core.settings.Settings.bold_text`
        num_to_df_display (int): Смотреть :attr:`~big5.modules.core.settings.Settings.num_to_df_display`
        text_runtime (str): Смотреть :attr:`~big5.modules.core.settings.Settings.text_runtime`
    """

    # ------------------------------------------------------------------------------------------------------------------
    # Конструктор
    # ------------------------------------------------------------------------------------------------------------------

    def __post_init__(self):
        super().__post_init__() # Выполнение конструктора из суперкласса

        self._trac_file: str = self._('Файл')
        self._trac_line: str = self._('Линия')
        self._trac_method: str = self._('Метод')
        self._trac_type_err: str = self._('Тип ошибки')

        self._sec: str = self._('сек.')

        self._folder_not_found: str = self._oh + self._('директория "{}" не найдена ...')
        self._file_not_found: str = self._oh + self._('файл "{}" не найден ...')
        self._directory_inst_file: str = self._oh + self._('вместо файла передана директория "{}" ...')
        self.no_acoustic_signal: str = self._oh + self._('файл "{}" не содержит акустического сигнала ...')

        self._files_not_found: str = self._oh + self._('в указанной директории необходимые файлы не найдены ...')

# ######################################################################################################################
# Ядро модулей
# ######################################################################################################################
@dataclass
class Core(CoreMessages):
    """Класс-ядро модулей

    Args:
        lang (str): Смотреть :attr:`~big5.modules.core.language.Language.lang`
        color_simple (str): Смотреть :attr:`~big5.modules.core.settings.Settings.color_simple`
        color_info (str): Смотреть :attr:`~big5.modules.core.settings.Settings.color_info`
        color_err (str): Смотреть :attr:`~big5.modules.core.settings.Settings.color_err`
        bold_text (bool): Смотреть :attr:`~big5.modules.core.settings.Settings.bold_text`
        num_to_df_display (int): Смотреть :attr:`~big5.modules.core.settings.Settings.num_to_df_display`
        text_runtime (str): Смотреть :attr:`~big5.modules.core.settings.Settings.text_runtime`
    """

    # ------------------------------------------------------------------------------------------------------------------
    # Конструктор
    # ------------------------------------------------------------------------------------------------------------------

    def __post_init__(self):
        super().__post_init__() # Выполнение конструктора из суперкласса

        self._start_time: int = -1 # Старт времени выполнения
        self._runtime: int = -1 # Время выполнения

        self._notebook_history_output: List[str] = [] # История вывода сообщений в ячейке Jupyter

        self._df_pkgs: pd.DataFrame = pd.DataFrame() # DataFrame c версиями установленных библиотек

        # Персональные качества личности человека (Порядок только такой)
        self._b5: Dict[str, Tuple[str, ...]] = {
            'en': ('openness', 'conscientiousness', 'extraversion', 'agreeableness', 'neuroticism'),
            'ru': (self._('открытость опыту'), self._('добросовестность'), self._('экстраверсия'),
                   self._('доброжелательность'), self._('нейротизм'))
        }

        self._df_files: pd.DataFrame = pd.DataFrame() # DataFrame с данными
        self._dict_of_files: Dict[List[str]] = {} # Словарь для DataFrame с данными

        self._mul: str = '&#10005;' # Знак умножения

        self._keys_id: str = 'ID' # Идентификатор

        # ----------------------- Только для внутреннего использования внутри класса

        self.__tab: str = '&nbsp;' * 4 # Табуляция (в виде пробелов)

    # ------------------------------------------------------------------------------------------------------------------
    # Свойства
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def is_notebook_(self) -> bool:
        """Получение результата определения запуска библиотеки в Jupyter или аналогах

        Returns:
            bool: **True** если библиотека запущена в Jupyter или аналогах, в обратном случае **False**

        Example:
            .. code-cell:: python
                :execution-count: 1
                :linenos:

                from big5.modules.core.core import Core

                core = Core()
                print(core.is_notebook_)

            .. output-cell::
                :execution-count: 1
                :linenos:

                True
        """

        return self.__is_notebook()

    # Получение времени выполнения
    @property
    def runtime_(self):
        """Получение времени выполнения

        Returns:
            int: Время выполнения
        """

        return self._runtime

    @property
    def df_pkgs_(self) -> pd.DataFrame:
        """Получение DataFrame c версиями установленных библиотек

        Returns:
            pd.DataFrame: **DataFrame** c версиями установленных библиотек
        """

        return self._df_pkgs

    @property
    def df_files_(self) -> pd.DataFrame:
        """Получение DataFrame c данными

        Returns:
            pd.DataFrame: **DataFrame** c данными
        """

        return self._df_files

    # ------------------------------------------------------------------------------------------------------------------
    # Внутренние методы (сообщения)
    # ------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def _traceback() -> Dict:
        """Трассировка исключений

        .. note::
            protected (защищенный метод)

        Returns:
            Dict: Словарь с описанием исключения
        """

        exc_type, exc_value, exc_traceback = sys.exc_info() # Получение информации об ошибке

        _trac = {
            'filename': exc_traceback.tb_frame.f_code.co_filename,
            'lineno': exc_traceback.tb_lineno,
            'name': exc_traceback.tb_frame.f_code.co_name,
            'type': exc_type.__name__
        }

        return _trac

    def _notebook_display_markdown(self, message: str, last: bool = False, out: bool = True) -> None:
        """Отображение сообщения

        .. note::
            protected (защищенный метод)

        Args:
            message (str): Сообщение
            last (bool): Замена последнего сообщения
            out (bool): Отображение

        Returns:
            None
        """

        if self.is_notebook_ is True:
            self._add_notebook_history_output(message, last) # Добавление истории вывода сообщений в ячейке Jupyter

            if type(out) is not bool: out = True

            if out is True: display(Markdown(message)) # Отображение

    def _metadata_info(self, last: bool = False, out: bool = True) -> None:
        """Информация об библиотеке

        .. note::
            protected (защищенный метод)

        Args:
            last (bool): Замена последнего сообщения
            out (bool): Отображение

        Returns:
            None
        """

        if self.is_notebook_ is True:
            tab = self.__tab

            b = '**' if self.bold_text_ is True else ''
            cr = self.color_simple_

            generate_name_with_email = lambda list1, list2: ''.join(
                map(str, map(
                    lambda l1, l2: f'<br /><span style=\"color:{cr}\">{tab * 2}{l1} [<u>{l2}</u>]</span>',
                    list1.split(', '), list2.split(', ')
                ))
            )

            author = generate_name_with_email(
                big5.__author__ru__ if self.lang_ == 'ru' else big5.__author__en__, big5.__email__
            )
            maintainer = generate_name_with_email(
                big5.__maintainer__ru__ if self.lang_ == 'ru' else big5.__maintainer__en__, big5.__maintainer_email__
            )

            # Отображение сообщения
            self._notebook_display_markdown(('{}' * 8).format(
                f'<span style=\"color:{self.color_simple_}\">{b}[</span><span style=\"color:{self.color_info_}\">',
                datetime.now().strftime(self._format_time),
                f'</span><span style=\"color:{self.color_simple_}\">]</span> ',
                f'<span style=\"color:{self.color_simple_}\">{self._metadata[0]}:</span>{b}',
                f'<br /><span style=\"color:{cr}\">{tab}{self._metadata[1]}:</span>{author}',
                f'<br /><span style=\"color:{cr}\">{tab}{self._metadata[2]}:</span>{maintainer}',
                f'<br /><span style=\"color:{cr}\">{tab}{self._metadata[3]}: <u>{big5.__release__}</u></span>',
                f'<br /><span style=\"color:{cr}\">{tab}{self._metadata[4]}: <u>{big5.__license__}</u></span></p>'
            ), last, out)

    def _inv_args(self, class_name: str, build_name: str, last: bool = False, out: bool = True) -> None:
        """Сообщение об указании неверных типов аргументов

        .. note::
            protected (защищенный метод)

        Args:
            class_name (str): Имя класса
            build_name (str): Имя метода/функции
            last (bool): Замена последнего сообщения
            out (bool): Отображение

        Returns:
            None
        """

        if self.is_notebook_ is True:
            inv_args = self._invalid_arguments.format(class_name + '.' + build_name)

            b = '**' if self.bold_text_ is True else ''

            # Отображение сообщения
            self._notebook_display_markdown('{}[{}{}{}] {}{}'.format(
                f'<span style=\"color:{self.color_simple_}\">{b}',
                f'</span><span style=\"color:{self.color_err_}\">',
                datetime.now().strftime(self._format_time),
                f'</span><span style=\"color:{self.color_simple_}\">', inv_args, f'{b}</span>'
            ), last, out)

    def _info(self, message: str, last: bool = False, out: bool = True) -> None:
        """Информационное сообщение

        .. note::
            protected (защищенный метод)

        Args:
            message (str): Сообщение
            last (bool): Замена последнего сообщения
            out (bool): Отображение

        Returns:
            None
        """

        if self.is_notebook_ is True:
            b = '**' if self.bold_text_ is True else ''

            # Отображение сообщения
            self._notebook_display_markdown(('{}' * 4).format(
                f'<span style=\"color:{self.color_simple_}\">{b}[</span><span style=\"color:{self.color_info_}\">',
                datetime.now().strftime(self._format_time),
                f'</span><span style=\"color:{self.color_simple_}\">]</span> ',
                f'<span style=\"color:{self.color_simple_}\">{message}</span>{b} '
            ), last, out)

    def _info_wrapper(self, message: str) -> str:
        """Обернутое информационное сообщение

        .. note::
            protected (защищенный метод)

        Args:
            message (str): Сообщение

        Returns:
            str: Обернутое информационное сообщение
        """

        if self.is_notebook_ is True:
            return ('{}' * 3).format(f'<span style=\"color:{self.color_info_}\">', message, f'</span>')

    def _bold_wrapper(self, message: str) -> str:
        """Обернутое сообщение с жирным начертанием

        .. note::
            protected (защищенный метод)

        Args:
            message (str): Сообщение

        Returns:
            str: Обернутое сообщение с жирным начертанием
        """

        if self.is_notebook_ is True:
            b = '**' if self.bold_text_ is True else ''

            return ('{}' * 3).format(f'<span>{b}', message, f'{b}</span>')

    def _error(self, message: str, last: bool = False, out: bool = True) -> None:
        """Сообщение об ошибке

        .. note::
            protected (защищенный метод)

        Args:
            message (str): Сообщение
            last (bool): Замена последнего сообщения
            out (bool): Отображение

        Returns:
            None
        """

        if self.is_notebook_ is True:
            b = '**' if self.bold_text_ is True else ''

            # Отображение сообщения
            self._notebook_display_markdown('{}[{}{}{}] {}{}'.format(
                f'<span style=\"color:{self.color_simple_}\">{b}', f'</span><span style=\"color:{self.color_err_}\">',
                datetime.now().strftime(self._format_time),
                f'</span><span style=\"color:{self.color_simple_}\">', message, f'{b}</span>'
            ), last, out)

    def _other_error(self, message: str, last: bool = False, out: bool = True) -> None:
        """Сообщение об прочей ошибке

        .. note::
            protected (защищенный метод)

        Args:
            message (str): Сообщение
            last (bool): Замена последнего сообщения
            out (bool): Отображение

        Returns:
            None
        """

        if self.is_notebook_ is True:
            trac = self._traceback() # Трассировка исключений

            b = '**' if self.bold_text_ is True else ''
            cr = self.color_simple_

            # Отображение сообщения
            self._notebook_display_markdown(('{}' * 8).format(
                f'<span style=\"color:{cr}\">{b}[</span><span style=\"color:{self.color_err_}\">',
                datetime.now().strftime(self._format_time),
                f'</span><span style=\"color:{cr}\">]</span> ',
                f'<span style=\"color:{cr}\">{message}</span>{b}',
                f'<p><span style=\"color:{cr}\">{self.__tab}{self._trac_file}: <u>{trac["filename"]}</u></span>',
                f'<br /><span style=\"color:{cr}\">{self.__tab}{self._trac_line}: <u>{trac["lineno"]}</u></span>',
                f'<br /><span style=\"color:{cr}\">{self.__tab}{self._trac_method}: <u>{trac["name"]}</u></span>',
                f'<br /><span style=\"color:{cr}\">{self.__tab}{self._trac_type_err}: <u>{trac["type"]}</u></span></p>'
            ), last, out)

    def _error_wrapper(self, message: str) -> str:
        """Обернутое сообщение об ошибке

        .. note::
            protected (защищенный метод)

        Args:
            message (str): Сообщение

        Returns:
            str: Обернутое сообщение об ошибке
        """

        if self.is_notebook_ is True:
            return ('{}' * 3).format(f'<span style=\"color:{self.color_err_}\">', message, f'</span>')

    def _stat_acoustic_features(self, message: str, last: bool = False, out: bool = True,
                                **kwargs: Union[int, Tuple[int], tf.TensorShape]) -> None:
        """Сообщение c статистикой извлеченных признаков из акустического сигнала

        .. note::
            protected (защищенный метод)

        Args:
            message (str): Сообщение
            last (bool): Замена последнего сообщения
            out (bool): Отображение
            **kwargs (int): Дополнительные именованные аргументы

        Returns:
            None
        """

        if self.is_notebook_ is True:
            tab = self.__tab

            b = '**' if self.bold_text_ is True else ''
            cr = self.color_simple_

            # Отображение сообщения
            self._notebook_display_markdown(message.format(
                f'<span style=\"color:{cr}\">{b}[</span><span style=\"color:{self.color_info_}\">',
                datetime.now().strftime(self._format_time),
                f'</span><span style=\"color:{cr}\">]</span> ',
                f'{b}<br /><span style=\"color:{cr}\">{tab}</span>',
                f'<br /><span style=\"color:{cr}\">{tab * 2}', f'<u>{kwargs["len_hc_features"]}</u></span>',
                f'<br /><span style=\"color:{cr}\">{tab * 2}', f'<u>{kwargs["len_melspectrogram_features"]}</u></span>',
                f'<br /><span style=\"color:{cr}\">{tab}',
                f'<u>{kwargs["shape_hc_features"][0]}</u>', f'<u>{kwargs["shape_hc_features"][1]}</u></span>',
                f'<br /><span style=\"color:{cr}\">{tab}',
                f' <u>{kwargs["shape_melspectrogram_features"][0]}</u>',
                f'<u>{kwargs["shape_melspectrogram_features"][1]}</u>',
                f'<u>{kwargs["shape_melspectrogram_features"][2]}</u></span>',
            ), last, out)

    def _r_start(self) -> None:
        """Начало отсчета времени выполнения

        .. note::
            protected (защищенный метод)

        Returns:
            None
        """

        self._runtime = self._start_time = -1 # Сброс значений

        self._start_time = time.time() # Отсчет времени выполнения

    def _r_end(self, last: bool = False, out: bool = True) -> None:
        """Конец отсчета времени выполнения

        .. note::
            protected (защищенный метод)

        Args:
            last (bool): Замена последнего сообщения
            out (bool): Отображение

        Returns:
            None
        """

        self._runtime = round(time.time() - self._start_time, 3) # Время выполнения

        t = '--- {}: {} {} ---'.format(self.text_runtime_, self._runtime, self._sec)

        if self.is_notebook_ is True:
            b = '**' if self.bold_text_ is True else ''

            # Отображение сообщения
            self._notebook_display_markdown(
                '{}'.format(f'<span style=\"color:{self.color_simple_}\">{b}{t}{b}</span>'), last, out)

    def _progressbar(self, message: str, progress: str, last: bool = False, out: bool = True) -> None:
        """Индикатор выполнения

        .. note::
            protected (защищенный метод)

        Args:
            message (str): Сообщение
            progress (str): Индикатор выполнения
            last (bool): Замена последнего сообщения
            out (bool): Отображение

        Returns:
            None
        """

        if self.is_notebook_ is True:
            b = '**' if self.bold_text is True else ''
            tab = self.__tab

            # Отображение сообщения
            self._notebook_display_markdown(('{}' * 5).format(
                f'<span style=\"color:{self.color_simple_}\">{b}[</span><span style=\"color:{self.color_info_}\">',
                datetime.now().strftime(self._format_time),
                f'</span><span style=\"color:{self.color_simple_}\">]</span> ',
                f'<span style=\"color:{self.color_simple_}\">{message}</span>{b}',
                f'<p><span style=\"color:{self.color_simple_}\">{tab}{progress}</span></p>'
            ), last, out)

    def _clear_notebook_history_output(self) -> None:
        """Очистка истории вывода сообщений в ячейке Jupyter

        .. note::
            protected (защищенный метод)

        Returns:
            None
        """

        self._notebook_history_output.clear() # Очистка истории вывода сообщений в ячейке Jupyter

    def _add_notebook_history_output(self, message: str, last: bool = False) -> None:
        """Добавление истории вывода сообщений в ячейке Jupyter

        .. note::
            protected (защищенный метод)

        Args:
            message (str): Сообщение
            last (bool): Замена последнего сообщения

        Returns:
            None
        """

        if last is True: self._notebook_history_output[-1] = message
        else: self._notebook_history_output.append(message)

    def _del_last_el_notebook_history_output(self) -> None:
        """Удаление последнего сообщения из истории вывода сообщений в ячейке Jupyter

        .. note::
            protected (защищенный метод)

        Returns:
            None
        """

        last_el = self._notebook_history_output.pop()

    def _add_last_el_notebook_history_output(self, message: str) -> None:
        """Добавление текста к последнему сообщению из истории вывода сообщений в ячейке Jupyter

        .. note::
            protected (защищенный метод)

        Args:
            message (str): Сообщение

        Returns:
            None
        """

        self._notebook_history_output[-1] += ' ' + message

    # ------------------------------------------------------------------------------------------------------------------
    # Внутренние методы (приватные)
    # ------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def __is_notebook() -> bool:
        """Определение запуска библиотеки в Jupyter или аналогах

        .. note::
            private (приватный метод)

        Returns:
            bool: **True** если библиотека запущена в Jupyter или аналогах, в обратном случае **False**
        """

        try:
            # Определение режима запуска библиотеки
            shell = get_ipython().__class__.__name__
        except (NameError, Exception): return False # Запуск в Python
        else:
            if shell == 'ZMQInteractiveShell' or shell == 'Shell': return True
            elif shell == 'TerminalInteractiveShell': return False
            else: return False

    # ------------------------------------------------------------------------------------------------------------------
    # Внутренние методы (защищенные)
    # ------------------------------------------------------------------------------------------------------------------
    def _get_paths(self, path: Iterable, depth: int = 1, out: bool = True) -> Union[List[str], bool]:
        """Получение директорий где хранятся данные

        .. note::
            protected (защищенный метод)

        Args:
            path (Iterable): Директория набора данных
            depth (int): Глубина иерархии для извлечения классов
            out (bool): Отображение

        Returns:
            Union[List[str], bool]: **False** если проверка аргументов не удалась или список с директориями
        """

        try:
            # Проверка аргументов
            if not isinstance(path, Iterable) or type(depth) is not int or depth < 1 or type(out) is not bool:
                raise TypeError
        except TypeError: self._other_error(self._som_ww, out = out); return False
        except Exception: self._other_error(self._unknown_err, out = out); return False
        else:
            if type(path) is not list: path = [path]

            new_path = [] # Список с директориями

            # Проход по всем директориям набора данных
            for curr_path in path:
                for f in os.scandir(str(curr_path)):
                    if f.is_dir() and not f.name.startswith('.'):
                        ignore = False # По умолчанию не игнорировать директорию
                        if depth == 1:
                            for curr_dir in self.ignore_dirs_:
                                if type(curr_dir) is not str: continue
                                if re.search('^' + curr_dir, f.name) is not None: ignore = True # Игнорировать директорию

                        if ignore is False: new_path.append(f.path)
            # Рекурсивный переход на следующий уровень иерархии
            if depth != 1: return self._get_paths(new_path, depth - 1)

            return new_path # Список с директориями

    def _append_to_list_of_files(self, path: str, preds: List[float], out: bool = True) -> bool:
        """Добавление значений в словарь для DataFrame c данными

        .. note::
            protected (защищенный метод)

        Аргументы:
            path (str): Путь к файлу
            preds (List[float]): Предсказания персональных качеств
            out (bool): Отображение

        Returns:
            bool: **True** если значения в словарь для DataFrame были добавлены, в обратном случае **False**
        """

        try:
           self._dict_of_files[self.keys_dataset_[0]].append(path)

           for i in range(len(preds)): self._dict_of_files[self.keys_dataset_[i + 1]].append(preds[i])
        except IndexError: self._other_error(self._som_ww, out = out); return False
        except Exception: self._other_error(self._unknown_err, out = out); return False
        else: return True

    # ------------------------------------------------------------------------------------------------------------------
    # Внешние методы
    # ------------------------------------------------------------------------------------------------------------------

    def show_notebook_history_output(self) -> None:
        """Отображение истории вывода сообщений в ячейке Jupyter

        Returns:
            None
        """

        if self.is_notebook_ is True and len(self._notebook_history_output) > 0:
            # Отображение
            for e in self._notebook_history_output: display(e if isinstance(e, pd.DataFrame) else Markdown(e))

    def libs_vers(self, runtime: bool = True, run: bool = True) -> None:
        """Получение и отображение версий установленных библиотек

        Args:
            runtime (bool): Подсчет времени выполнения
            run (bool): Блокировка выполнения

        Returns:
            None
        """

        self._clear_notebook_history_output() # Очистка истории вывода сообщений в ячейке Jupyter

        # Сброс
        self._df_pkgs = pd.DataFrame() # Пустой DataFrame

        try:
            # Проверка аргументов
            if type(runtime) is not bool or type(run) is not bool: raise TypeError
        except TypeError: self._inv_args(__class__.__name__, self.libs_vers.__name__)
        else:
            # Блокировка выполнения
            if run is False: self._error(self._lock_user); return None

            if runtime: self._r_start()

            pkgs = {
                'Package': [
                    'TensorFlow', 'Keras', 'NumPy', 'Pandas', 'Scikit-learn', 'OpenSmile', 'Librosa', 'AudioRead',
                    'IPython', 'Requests', 'JupyterLab'
                ],
                'Version': [i.__version__ for i in [
                    tf, keras, np, pd, sklearn, opensmile, librosa, audioread, IPython, requests, jlab
                ]]
            }

            self._df_pkgs = pd.DataFrame(data = pkgs) # Версии используемых библиотек
            self._df_pkgs.index += 1

            # Отображение
            if self.is_notebook_ is True: display(self._df_pkgs)

            if runtime: self._r_end()