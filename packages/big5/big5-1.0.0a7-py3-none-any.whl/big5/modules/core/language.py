# -*- coding: utf-8 -*-

"""
Определение языка
"""

# ######################################################################################################################
# Импорт необходимых инструментов
# ######################################################################################################################
# Интернационализация (I18N) и локализация (L10N) (см. https://www.loc.gov/standards/iso639-2/php/code_list.php)
#     - brew install gettext (Если не установлен)
#     - brew link gettext --force
#     1. gettext --help
#     2. locate pygettext.py
#     3. /usr/local/Cellar/python@3.9/3.9.7/Frameworks/Python.framework/Versions/3.9/share/doc/python3.9/examples/Tools/
#        i18n/pygettext.py -d big5 -o big5/modules/locales/base.pot big5
#     4. msgfmt --help
#     5. locate msgfmt.py
#     6. /usr/local/Cellar/python@3.9/3.9.7/Frameworks/Python.framework/Versions/3.9/share/doc/python3.9/examples/Tools/
#        i18n/msgfmt.py big5/modules/locales/en/LC_MESSAGES/base.po big5/modules/locales/en/LC_MESSAGES/base
# Подавление Warning
import warnings
for warn in [UserWarning, FutureWarning]: warnings.filterwarnings('ignore', category = warn)

from dataclasses import dataclass # Класс данных

import os      # Взаимодействие с файловой системой
import gettext # Формирование языковых пакетов
import inspect # Инспектор

# Типы данных
from typing import List, Dict, Optional
from types import MethodType

# ######################################################################################################################
# Интернационализация (I18N) и локализация (L10N)
# ######################################################################################################################
@dataclass
class Language:
    """Класс для интернационализации (I18N) и локализации (L10N)

    Args:
        lang (str): Язык
    """

    # ------------------------------------------------------------------------------------------------------------------
    # Конструктор
    # ------------------------------------------------------------------------------------------------------------------

    lang: str = 'ru'
    """
    str: Язык, доступные варианты:

        * ``"ru"`` - Русский язык (``по умолчанию``)
        * ``"en"`` - Английский язык
    """

    def __post_init__(self):
        # Директория с поддерживаемыми языками
        self.__path_to_locales: str = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'locales'))
        self.__locales: List[str] = self.__get_languages()  # Поддерживаемые языки

        self.__lang: str = self.lang # Язык

        self.__i18n: Dict[str, MethodType] = self.__get_locales() # Получение языковых пакетов

        self._: MethodType = self.__set_locale(self.lang_) # Установка языка


    # ------------------------------------------------------------------------------------------------------------------
    # Свойства
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def lang_(self) -> str:
        """Получение текущего языка

        Returns:
            str: Язык

        Example:
            .. code-cell:: python
                :execution-count: 1
                :linenos:

                from big5.modules.core.language import Language

                language = Language(lang = 'en')
                print(language.lang_)

            .. output-cell::
                :execution-count: 1
                :linenos:

                en
        """

        try:
            # Проверка аргументов
            if type(self.__lang) is not str or not self.__lang or (self.__lang in self.locales_) is False:
                raise TypeError
        except TypeError: return 'ru'
        else: return self.__lang

    @property
    def path_to_locales_(self) -> str:
        """Получение директории с языковыми пакетами

        Returns:
            str: Директория с языковыми пакетами

        Example:
            .. code-cell:: python
                :execution-count: 1
                :linenos:

                from big5.modules.core.language import Language

                language = Language(lang = 'en')
                print(language.path_to_locales_)

            .. output-cell::
                :execution-count: 1
                :linenos:

                /Users/dl/GitHub/big5/big5/modules/locales
        """

        return os.path.normpath(self.__path_to_locales) # Нормализация пути

    @property
    def locales_(self) -> List[str]:
        """Получение поддерживаемых языков

        Returns:
            List[str]: Список поддерживаемых языков

        Example:
            .. code-cell:: python
                :execution-count: 1
                :linenos:

                from big5.modules.core.language import Language

                language = Language(lang = 'en')
                print(language.locales_)

            .. output-cell::
                :execution-count: 1
                :linenos:

                ['ru', 'en']
        """

        return self.__locales

    # ------------------------------------------------------------------------------------------------------------------
    # Внутренние методы
    # ------------------------------------------------------------------------------------------------------------------

    def __get_languages(self) -> List[Optional[str]]:
        """Получение поддерживаемых языков

        .. note::
            private (приватный метод)

        Returns:
            List[Optional[str]]: Список поддерживаемых языков
        """

        # Директория с языками найдена
        if os.path.exists(self.path_to_locales_):
            # Формирование списка с подерживаемыми языками
            return next(os.walk(self.path_to_locales_))[1]

        return []

    def __get_locales(self) -> Dict[str, MethodType]:
        """Получение языковых пакетов

        .. note::
            private (приватный метод)

        Returns:
             Dict[str, MethodType]: Словарь с языковыми пакетами
        """

        trs_base = {} # Языки

        # Проход по всем языкам
        for curr_lang in self.locales_:
            trs_base[curr_lang] = gettext.translation(
                'base', # Домен
                localedir = self.path_to_locales_, # Директория с поддерживаемыми языками
                languages = [curr_lang], # Язык
                fallback = True # Отключение ошибки
            ).gettext

            # self.__lang = curr_lang # Изменение языка

        return trs_base

    def __set_locale(self, lang: str = '') -> MethodType:
        """Установка языка

        .. note::
            private (приватный метод)

        Args:
            lang (str): Язык

        Returns:
             MethodType: MethodType перевода строк на один из поддерживаемых языков если метод запущен через конструктор
        """

        try:
            # Проверка аргументов
            if type(lang) is not str: raise TypeError
        except TypeError: pass
        else:
            # Проход по всем поддерживаемым языкам
            for curr_lang in self.locales_:
                # В аргументах метода не найден язык
                if lang != curr_lang: continue

                self.__lang = curr_lang # Изменение языка

            # Метод запущен в конструкторе
            if inspect.stack()[1].function == "__init__" or inspect.stack()[1].function == "__post_init__":
                return self.__i18n[self.lang_]
            else: self._ = self.__i18n[self.lang_] # Установка языка
