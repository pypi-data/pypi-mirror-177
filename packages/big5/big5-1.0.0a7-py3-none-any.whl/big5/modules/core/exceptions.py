#!/usr/bin/env python
# -*- coding: utf-8 -*-

class CustomException(Exception):
    """Класс для всех пользовательских исключений

    Example:
        .. code-cell:: python
            :execution-count: 1
            :linenos:

            from big5.modules.core.exceptions import CustomException

            try: raise CustomException('Пользовательское исключение')
            except CustomException as ex: print(ex)

        .. output-cell::
            :execution-count: 1
            :linenos:

            Пользовательское исключение
    """
    pass

class IsSmallWindowSizeError(CustomException):
    """Указан слишком маленький размер окна сегмента сигнала"""
    pass
