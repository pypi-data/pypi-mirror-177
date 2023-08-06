#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Аудио
"""

# ######################################################################################################################
# Импорт необходимых инструментов
# ######################################################################################################################
# Подавление Warning
import warnings
for warn in [UserWarning, FutureWarning]: warnings.filterwarnings('ignore', category = warn)

from dataclasses import dataclass # Класс данных

import os           # Взаимодействие с файловой системой
import logging
import requests     # Отправка HTTP запросов
import numpy as np  # Научные вычисления
import pandas as pd # Обработка и анализ данных
import opensmile    # Анализ, обработка и классификация звука
import librosa      # Обработка аудио
import audioread    # Декодирование звука
import math

from urllib.parse import urlparse
from pathlib import Path # Работа с путями в файловой системе
from sklearn import preprocessing

from typing import Dict, List, Tuple, Union, Callable # Типы данных

from IPython.display import clear_output

# Персональные
from big5.modules.lab.download import Download # Загрузка файлов
from big5.modules.core.exceptions import IsSmallWindowSizeError

# Порог регистрации сообщений TensorFlow
logging.disable(logging.WARNING)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import tensorflow as tf # Машинное обучение от Google
import keras

from tensorflow.keras.applications import VGG16

# ######################################################################################################################
# Сообщения
# ######################################################################################################################
@dataclass
class  AudioMessages(Download):
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

        self._curr_progress_audio_union_predictions: str = '{} ' + self._from_precent + ' {} ({}%) ... {} ...'

        self._formation_model_hc: str = self._('Формирование нейросетевой архитектуры модели для получения оценок по '
                                               'экспертным признакам ...')
        self._formation_model_spec: str = self._('Формирование нейросетевой архитектуры для получения оценок по '
                                                 'нейросетевым признакам ...')
        self._formation_models_b5: str = self._('Формирование нейросетевых архитектур моделей для получения результатов'
                                                ' оценки персональных качеств ...')

        self._load_model_weights_hc: str = self._('Загрузка весов нейросетевой модели для получения оценок по '
                                                  'экспертным признакам ...')
        self._load_model_weights_spec: str = self._('Загрузка весов нейросетевой модели для получения оценок по '
                                                    'нейросетевым признакам ...')
        self._load_models_weights_b5: str = self._('Загрузка весов нейросетевых моделей для получения результатов '
                                                   'оценки персональных качеств ...')
        self._load_model_weights_error: str = self._oh + self._('не удалось загрузить веса нейросетевой модели ...')

        self._get_acoustic_feature_info: str = self._('Извлечение признаков (экспертных и лог мел-спектрограмм) из '
                                                      'акустического сигнала ...')
        self._get_acoustic_feature_stat: str = '{}' * 3 + \
                                               self._('Статистика извлеченных признаков из акустического сигнала:'
                                                      '{}Общее количество сегментов с:'
                                                      '{}1. экспертными признаками: {}'
                                                      '{}2. лог мел-спектрограммами: {}'
                                                      '{}Размерность матрицы экспертных признаков одного сегмента: '
                                                      '{} ' + self._mul + ' {}'
                                                      '{}Размерность тензора с лог мел-спектрограммами одного сегмента:'
                                                      '{} ' + self._mul + ' {} ' + self._mul + ' {}')

        self._window_small_size_error: str = self._oh + self._('указан слишком маленький размер ({}) окна сегмента '
                                                               'сигнала ...')

        self._get_audio_union_predictions_info: str = self._('Получение прогнозов (аудио модальность) ...')

        self._audio_model_hc_not_formation: str = self._oh + self._('нейросетевая архитектура модели для получения '
                                                                    'оценок по экспертным признакам не сформирована '
                                                                    '...')
        self._audio_model_spec_not_formation: str = self._oh + self._('нейросетевая архитектура модели для получения '
                                                                      'оценок по нейросетевым признакам не '
                                                                      'сформирована ...')
        self._audio_models_not_formation: str = self._oh + self._('нейросетевые архитектуры моделей для получения '
                                                                  'оценок по экспертным и нейросетевым признакам не '
                                                                  'сформированы ...')

# ######################################################################################################################
# Аудио
# ######################################################################################################################
@dataclass
class Audio(AudioMessages):
    """Класс для обработки аудио

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

        # Нейросетевая модель **tf.keras.Model** для получения оценок по экспертным признакам
        self._audio_model_hc: Union[keras.engine.functional.Functional, None] = None
        # Нейросетевая модель **tf.keras.Model** для получения оценок по нейросетевым признакам
        self._audio_model_spec: Union[keras.engine.functional.Functional, None] = None
        # Нейросетевые модели **tf.keras.Model** для получения результатов оценки персональных качеств
        self._audio_models_b5: Dict[str, Union[keras.engine.functional.Functional, None]] = dict(zip(
            self._b5['en'], [None] * len(self._b5['en'])
        ))

        self._smile: opensmile.core.smile.Smile = self.__smile() # Извлечение функций OpenSmile

        # Веса для нейросетевых архитектур
        self._weights_for_big5: Dict[str, Dict] = {
            'audio': {
                'hc': {
                    'sberdisk': 'https://files.sberdisk.ru/s/MMRrak8fMsyzxLE/download',
                },
                'spec': {
                    'sberdisk': 'https://files.sberdisk.ru/s/W6LCtD33FQHnYEz/download',
                },
                'b5': {
                    'openness': {
                        'sberdisk': 'https://files.sberdisk.ru/s/443WRA9MFWqWBAE/download',
                    },
                    'conscientiousness': {
                        'sberdisk': 'https://files.sberdisk.ru/s/eDG28m3H6c8bWoE/download',
                    },
                    'extraversion': {
                        'sberdisk': 'https://files.sberdisk.ru/s/3daBSTYnmZaesee/download',
                    },
                    'agreeableness': {
                        'sberdisk': 'https://files.sberdisk.ru/s/52ZPHMjb4CFmdYa/download',
                    },
                    'neuroticism': {
                        'sberdisk': 'https://files.sberdisk.ru/s/q8CZJ99rZqcNxkM/download',
                    },
                },
            },
        }

        # ----------------------- Только для внутреннего использования внутри класса

        # Настройки для спектрограммы
        self.__pl: List[Union[int, str, bool, float, None]] = [
            2048, 512, None, True, 'reflect', 2.0, 128, 'slaney', True, None
        ]
        self.__len_paths: int = 0 # Количество искомых файлов
        self.__local_path: Union[Callable[[str], str], None] = None # Локальный путь

    # ------------------------------------------------------------------------------------------------------------------
    # Свойства
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def audio_model_hc_(self) -> Union[keras.engine.functional.Functional, None]:
        """Получение нейросетевой модели **tf.keras.Model** для получения оценок по экспертным признакам

        Returns:
            keras.engine.functional.Functional or None: Нейросетевой модели **tf.keras.Model** или None
        """

        return self._audio_model_hc

    @property
    def audio_model_spec_(self) -> Union[keras.engine.functional.Functional, None]:
        """Получение нейросетевой модели **tf.keras.Model** для получения оценок по нейросетевым признакам

        Returns:
            keras.engine.functional.Functional or None: Нейросетевой модели **tf.keras.Model** или None
        """

        return self._audio_model_spec

    def audio_models_b5_(self) -> Dict:
        """Получение нейросетевых моделей **tf.keras.Model** для получения результатов оценки персональных качеств

        Returns:
            Dict: Словарь с нейросетевыми моделями **tf.keras.Model**
        """

        return self._audio_models_b5

    @property
    def weights_for_big5_(self) -> Dict:
        """Получение весов для нейросетевых архитектур

        Returns:
            Dict: Словарь с весами для нейросетевых архитектур
        """

        return self._weights_for_big5

    @property
    def smile_(self) -> Union[opensmile.core.smile.Smile, None]:
        """Получение функций OpenSmile

        Returns:
            opensmile.core.smile.Smile: Извлеченные функции OpenSmile
        """

        return self._smile

    # ------------------------------------------------------------------------------------------------------------------
    # Внутренние методы (приватные)
    # ------------------------------------------------------------------------------------------------------------------

    def __load_model_weights(
        self, url: str, force_reload: bool = True, info_text: str = '',
            out: bool = True, runtime: bool = True, run: bool = True
    ) -> bool:
        """Загрузка весов нейросетевой модели

        .. note::
            private (приватный метод)

        Args:
            url (str): Полный путь к файлу с весами нейросетевой модели
            force_reload (bool): Принудительная загрузка файла с весами нейросетевой модели из сети
            info_text (str): Текст для информационного сообщения
            out (bool): Отображение
            runtime (bool): Подсчет времени выполнения
            run (bool): Блокировка выполнения

        Returns:
            bool: **True** если веса нейросетевой модели загружены, в обратном случае **False**
        """

        self._clear_notebook_history_output() # Очистка истории вывода сообщений в ячейке Jupyter

        try:
            # Проверка аргументов
            if (type(url) is not str or not url or type(force_reload) is not bool
                or type(info_text) is not str or not info_text or type(out) is not bool
                or type(runtime) is not bool or type(run) is not bool): raise TypeError
        except TypeError:
            self._inv_args(__class__.__name__, self.__load_model_weights.__name__, out = out); return False
        else:
            # Блокировка выполнения
            if run is False: self._error(self._lock_user, out = out); return False

            if runtime: self._r_start()

            # Информационное сообщение
            self._info(info_text, last = False, out = False)

            sections = urlparse(url) # Парсинг URL адреса

            try:
                # URL файл невалидный
                if sections.scheme == '': raise requests.exceptions.InvalidURL
            except requests.exceptions.InvalidURL:
                url = os.path.normpath(url)

                try:
                    if os.path.isfile(url) is False: raise FileNotFoundError # Не файл
                except FileNotFoundError: self._other_error(self._load_model_weights_error, out = out); return False
                except Exception: self._other_error(self._unknown_err, out = out); return False
                else:
                    self._url_last_filename = url
                    if out: self.show_notebook_history_output() # Отображение истории вывода сообщений в ячейке Jupyter
            else:
                try:
                    # Загрузка файла из URL
                    res_download_file_from_url = self._download_file_from_url(
                        url = url, force_reload = force_reload, runtime = False, out = out, run = True
                    )
                except Exception: self._other_error(self._unknown_err, out = out); return False
                else:
                    # Файл загружен
                    if res_download_file_from_url != 200: return False

                    return True
            finally:
                if runtime: self._r_end(out = out)

    @staticmethod
    def __smile() -> opensmile.core.smile.Smile:
        """Извлечение функций OpenSmile

        .. note::
            private (приватный метод)

        Returns:
             opensmile.core.smile.Smile: Извлеченные функции OpenSmile
        """

        return opensmile.Smile(
            feature_set = opensmile.FeatureSet.eGeMAPSv02,
            feature_level = opensmile.FeatureLevel.LowLevelDescriptors,
        )

    def __progressbar_union_predictions(
            self, message: str, item: int, info: str, last: bool, len_paths: int, out: bool) -> None:
        """Индикатор выполнения получения прогнозов по аудио

        .. note::
            private (приватный метод)

        Аргументы:
            message (str): Сообщение
            item (int): Номер видеофайла
            info (str): Локальный путь
            last (bool): Замена последнего сообщения
            len_paths (int): Количество видеофайлов
            out (bool): Отображение

        Returns:
            None
        """

        clear_output(True)
        self._progressbar(
            message,
            self._curr_progress_audio_union_predictions.format(
                item, len_paths, round(item * 100 / len_paths, 2), info
            ),
            last = last, out = False
        )
        if out: self.show_notebook_history_output()

    @staticmethod
    def __norm_pred(pred_data: np.ndarray, len_spec: int = 16) -> np.ndarray:
        """Нормализация оценок по экспертным и нейросетевым признакам

        .. note::
            private (приватный метод)

        Аргументы:
            pred_data (np.ndarray): Оценки
            len_spec (int): Максимальный размер вектора оценок

        Returns:
            np.ndarray: Нормализованные оценки по экспертным и нейросетевым признакам
        """

        if pred_data.shape[0] < len_spec: return np.pad(pred_data, ((0, len_spec - pred_data.shape[0]), (0, 0)), 'mean')
        return pred_data[:len_spec]

    def __concat_pred(self, pred_hc: np.ndarray, pred_melspectrogram: np.ndarray) -> List[np.ndarray]:
        """Конкатенация оценок по экспертным и нейросетевым признакам

        .. note::
            private (приватный метод)

        Аргументы:
            pred_hc (np.ndarray): Оценки по экспертным признакам
            pred_melspectrogram (np.ndarray): Оценки по нейросетевым признакам

        Returns:
            List[np.ndarray]: Конкатенированные оценки по экспертным и нейросетевым признакам
        """

        # Нормализация оценок по экспертным и нейросетевым признакам
        pred_hc_norm = self.__norm_pred(pred_hc)
        pred_melspectrogram_norm = self.__norm_pred(pred_melspectrogram)

        concat = []

        # Проход по всем персональным качествам личности человека
        for i in range(len(self._b5['en'])):
            concat.append(np.hstack((np.asarray(pred_hc_norm)[:, i], np.asarray(pred_melspectrogram_norm)[:, i])))

        return concat

    @staticmethod
    def __load_audio_model_b5() -> keras.engine.functional.Functional:
        """Формирование нейросетевой архитектуры модели для получения результата оценки персонального качества

        .. note::
            private (приватный метод)

        Returns:
            keras.engine.functional.Functional:
                Нейросетевая модель **tf.keras.Model** для получения результата оценки персонального качества
        """

        input_1 = tf.keras.Input(shape = (32,), name = 'input_1')
        x = tf.keras.layers.Dense(units = 1, name = 'dense_1')(input_1)
        x = tf.keras.layers.Activation('sigmoid', name = 'activ_1')(x)

        model = tf.keras.Model(inputs = input_1, outputs = x)

        return model

    # ------------------------------------------------------------------------------------------------------------------
    # Внутренние методы (защищенные)
    # ------------------------------------------------------------------------------------------------------------------

    def _get_acoustic_features(self, path: str, sr: int = 44100, window: Union[int, float] = 2.0,
                             step: Union[int, float] = 1.0, last: bool = False, out: bool = True, runtime: bool = True,
                               run: bool = True) -> Tuple[List[Union[np.ndarray, None]], List[Union[np.ndarray, None]]]:
        """Извлечение признаков из акустического сигнала

        .. note::
            protected (защищенный метод)

        Args:
            path (str): Путь к аудио или видеофайлу
            sr (int): Частота дискретизации
            window (Union[int, float]): Размер окна сегмента сигнала (в секундах)
            step (Union[int, float]): Шаг сдвига окна сегмента сигнала (в секундах)
            last (bool): Замена последнего сообщения
            out (bool): Отображение
            runtime (bool): Подсчет времени выполнения
            run (bool): Блокировка выполнения

        Returns:
            Tuple[List[Union[np.ndarray, None]], List[Union[np.ndarray, None]]]: Кортеж с двумя списками:

                1. Список с экспертными признаками
                2. Список с лог мел-спектрограммами
        """

        try:
            # Проверка аргументов
            if (type(path) is not str or not path or type(sr) is not int or sr < 1
                    or ((type(window) is not int or window < 1) and (type(window) is not float or window <= 0))
                    or ((type(step) is not int or step < 1) and (type(step) is not float or step <= 0))
                    or type(last) is not bool or type(out) is not bool or type(runtime) is not bool
                    or type(run) is not bool): raise TypeError
        except TypeError:
            self._inv_args(__class__.__name__, self._get_acoustic_features.__name__, last = last, out = out)
            return [], []
        else:
            # Блокировка выполнения
            if run is False: self._error(self._lock_user, last = last, out = out); return [], []

            if runtime: self._r_start()

            if last is False:
                # Информационное сообщение
                self._info(self._get_acoustic_feature_info, out = False)
                if out: self.show_notebook_history_output() # Отображение истории вывода сообщений в ячейке Jupyter

            try:
                # Считывание аудио или видеофайла
                audio, sr = librosa.load(path = path, sr = sr)
            except FileNotFoundError:
                self._other_error(self._file_not_found.format(self._info_wrapper(path)), last = last, out = out)
                return [], []
            except IsADirectoryError:
                self._other_error(self._directory_inst_file.format(self._info_wrapper(path)), last = last, out = out)
                return [], []
            except audioread.NoBackendError:
                self._other_error(self.no_acoustic_signal.format(self._info_wrapper(path)), last = last, out = out)
                return [], []
            except Exception: self._other_error(self._unknown_err, last = last, out = out); return [], []
            else:
                hc_features = [] # Список с экспертными признаками
                melspectrogram_features = [] # Список с лог мел-спектрограммами

                try:
                    lhcf = int((window * 1000 - 40) / 10)

                    if lhcf < 2: raise IsSmallWindowSizeError
                except IsSmallWindowSizeError:
                    self._other_error(self._window_small_size_error.format(self._info_wrapper(str(window))),
                                      last = last, out = out)
                    return [], []
                except Exception: self._other_error(self._unknown_err, last = last, out = out); return [], []
                else:
                    window_local = int(sr * window)

                    len_spec = window_local / self.__pl[1]
                    if math.modf(len_spec)[0] == 0: len_spec += 1
                    len_spec = math.ceil(len_spec)

                    for cnt, val in enumerate(range(0, audio.shape[0] + 1, int(sr * step))):
                        val_end = val + window_local

                        curr_audio = audio[val:val_end] # Часть аудио

                        # Формирование экспертных признаков
                        hc_feature = self.smile_.process_signal(curr_audio, sr).to_numpy()

                        try:
                            # Нормализация экспертных признаков
                            hc_feature = preprocessing.normalize(hc_feature, norm = 'l2', axis = 0)
                        except Exception: pass
                        else:
                            # Дополнение экспертных признаков нулями
                            hc_feature = np.pad(hc_feature, ((0, lhcf - hc_feature.shape[0]), (0, 0)))
                            hc_features.append(hc_feature) # Добавление экспертных признаков в список

                        # Получение лог мел-спектрограмм
                        if len(curr_audio) > self.__pl[0]:
                            melspectrogram = librosa.feature.melspectrogram(
                                y          = curr_audio,
                                sr         = sr,
                                n_fft      = self.__pl[0],
                                hop_length = self.__pl[1],
                                win_length = self.__pl[2],
                                center     = self.__pl[3],
                                pad_mode   = self.__pl[4],
                                power      = self.__pl[5],
                                n_mels     = self.__pl[6],
                                norm       = self.__pl[7],
                                htk        = self.__pl[8],
                                fmax       = self.__pl[9]
                            )

                            # Преобразование спектрограммы из мощности (квадрат амплитуды) в децибелы (дБ)
                            melspectrogram_to_db = librosa.power_to_db(melspectrogram, top_db = 80)

                            if melspectrogram_to_db.shape[1] < len_spec:
                                melspectrogram_to_db = np.pad(
                                    melspectrogram_to_db,
                                    ((0, 0), (0, len_spec - melspectrogram_to_db.shape[1])),
                                    'mean'
                                )
                            melspectrogram_to_db /= 255 # Линейная нормализация
                            melspectrogram_to_db = np.expand_dims(melspectrogram_to_db, axis = -1)
                            melspectrogram_to_db = tf.image.resize(melspectrogram_to_db, (224, 224)) # Масштабирование
                            melspectrogram_to_db = tf.repeat(melspectrogram_to_db, 3, axis = -1) # GRAY -> RGB
                            # Добавление лог мел-спектрограммы в список
                            melspectrogram_features.append(melspectrogram_to_db)

                    if last is False:
                        # Статистика извлеченных признаков из акустического сигнала
                        self._stat_acoustic_features(
                            message = self._get_acoustic_feature_stat,
                            last = last, out = out,
                            len_hc_features = len(hc_features),
                            len_melspectrogram_features = len(melspectrogram_features),
                            shape_hc_features = hc_features[0].shape,
                            shape_melspectrogram_features = melspectrogram_features[0].shape
                        )

                    return hc_features, melspectrogram_features
            finally:
                if runtime: self._r_end(out = out)

    # ------------------------------------------------------------------------------------------------------------------
    # Внешние методы
    # ------------------------------------------------------------------------------------------------------------------

    def load_audio_model_hc(self, out: bool = True, runtime: bool = True, run: bool = True) -> bool:
        """Формирование нейросетевой архитектуры модели для получения оценок по экспертным признакам

        Args:
            out (bool): Отображение
            runtime (bool): Подсчет времени выполнения
            run (bool): Блокировка выполнения

        Returns:
            bool: **True** если нейросетевая архитектура модели сформирована, в обратном случае **False**
        """

        self._clear_notebook_history_output() # Очистка истории вывода сообщений в ячейке Jupyter

        try:
            # Проверка аргументов
            if type(out) is not bool or type(runtime) is not bool or type(run) is not bool: raise TypeError
        except TypeError: self._inv_args(__class__.__name__, self.load_audio_model_hc.__name__, out = out); return False
        else:
            # Блокировка выполнения
            if run is False: self._error(self._lock_user, out = out); return False

            if runtime: self._r_start()

            # Информационное сообщение
            self._info(self._formation_model_hc, last = False, out = False)
            if out: self.show_notebook_history_output() # Отображение истории вывода сообщений в ячейке Jupyter

            input_lstm = tf.keras.Input(shape = (196, 25))

            x = tf.keras.layers.LSTM(64, return_sequences = True)(input_lstm)
            x = tf.keras.layers.Dropout(rate = 0.2)(x)
            x = tf.keras.layers.LSTM(128, return_sequences = False)(x)
            x = tf.keras.layers.Dropout(rate = 0.2)(x)
            x = tf.keras.layers.Dense(5, activation = 'linear')(x)

            self._audio_model_hc = tf.keras.Model(inputs = input_lstm, outputs = x)

            if runtime: self._r_end()
        finally: return True

    def load_audio_model_spec(self, out: bool = True, runtime: bool = True, run: bool = True) -> bool:
        """Формирование нейросетевой архитектуры для получения оценок по нейросетевым признакам

        Args:
            out (bool): Отображение
            runtime (bool): Подсчет времени выполнения
            run (bool): Блокировка выполнения

        Returns:
            bool: **True** если нейросетевая архитектура модели сформирована, в обратном случае **False**
        """

        self._clear_notebook_history_output() # Очистка истории вывода сообщений в ячейке Jupyter

        try:
            # Проверка аргументов
            if type(out) is not bool or type(runtime) is not bool or type(run) is not bool: raise TypeError
        except TypeError:
            self._inv_args(__class__.__name__, self.load_audio_model_spec.__name__, out = out); return False
        else:
            # Блокировка выполнения
            if run is False: self._error(self._lock_user, out = out); return False

            if runtime: self._r_start()

            # Информационное сообщение
            self._info(self._formation_model_spec, last = False, out = False)
            if out: self.show_notebook_history_output() # Отображение истории вывода сообщений в ячейке Jupyter

            vgg_model = VGG16(weights = None, include_top = False, input_shape = (224, 224, 3))

            x = vgg_model.output
            x = tf.keras.layers.Flatten()(x)
            x = tf.keras.layers.Dense(512, activation = 'relu')(x)
            x = tf.keras.layers.Dropout(0.5)(x)
            x = tf.keras.layers.Dense(256, activation = 'relu')(x)
            x = tf.keras.layers.Dense(5, activation = 'linear')(x)

            self._audio_model_spec = tf.keras.models.Model(inputs = vgg_model.input, outputs = x)

            if runtime: self._r_end()
        finally: return True

    def load_audio_models_b5(self, out: bool = True, runtime: bool = True, run: bool = True) -> bool:
        """Формирование нейросетевых архитектур моделей для получения результатов оценки персональных качеств

        Args:
            out (bool): Отображение
            runtime (bool): Подсчет времени выполнения
            run (bool): Блокировка выполнения

        Returns:
            bool: **True** если нейросетевые архитектуры модели сформированы, в обратном случае **False**
        """

        self._clear_notebook_history_output() # Очистка истории вывода сообщений в ячейке Jupyter

        try:
            # Проверка аргументов
            if type(out) is not bool or type(runtime) is not bool or type(run) is not bool: raise TypeError
        except TypeError:
            self._inv_args(__class__.__name__, self.load_audio_models_b5.__name__, out = out); return False
        else:
            # Блокировка выполнения
            if run is False: self._error(self._lock_user, out = out); return False

            if runtime: self._r_start()

            # Информационное сообщение
            self._info(self._formation_models_b5, last = False, out = False)
            if out: self.show_notebook_history_output() # Отображение истории вывода сообщений в ячейке Jupyter

            for key, _ in self._audio_models_b5.items():
                self._audio_models_b5[key] = self.__load_audio_model_b5()

            if runtime: self._r_end()
        finally:
            return True

    def load_model_weights_hc(
            self, url: str, force_reload: bool = True, out: bool = True, runtime: bool = True, run: bool = True
    ) -> bool:
        """Загрузка весов нейросетевой модели для получения оценок по экспертным признакам

        Args:
            url (str): Полный путь к файлу с весами нейросетевой модели
            force_reload (bool): Принудительная загрузка файла с весами нейросетевой модели из сети
            out (bool): Отображение
            runtime (bool): Подсчет времени выполнения
            run (bool): Блокировка выполнения

        Returns:
            bool: **True** если веса нейросетевой модели загружены, в обратном случае **False**
        """

        if self.__load_model_weights(url, force_reload, self._load_model_weights_hc, out, runtime, run) is True:
            self._audio_model_hc.load_weights(self._url_last_filename)

            return True

        return False

    def load_model_weights_spec(
            self, url: str, force_reload: bool = True, out: bool = True, runtime: bool = True, run: bool = True
    ) -> bool:
        """Загрузка весов нейросетевой модели для получения оценок по нейросетевым признакам

        Args:
            url (str): Полный путь к файлу с весами нейросетевой модели
            force_reload (bool): Принудительная загрузка файла с весами нейросетевой модели из сети
            out (bool): Отображение
            runtime (bool): Подсчет времени выполнения
            run (bool): Блокировка выполнения

        Returns:
            bool: **True** если веса нейросетевой модели загружены, в обратном случае **False**
        """

        if self.__load_model_weights(url, force_reload, self._load_model_weights_spec, out, runtime, run) is True:
            self._audio_model_spec.load_weights(self._url_last_filename)

            return True

        return False

    def load_models_weights_b5(
            self, url_openness: str, url_conscientiousness: str, url_extraversion: str, url_agreeableness: str,
            url_neuroticism: str, force_reload: bool = True, out: bool = True, runtime: bool = True, run: bool = True
    ) -> bool:
        """Загрузка весов нейросетевых моделей для получения результатов оценки персональных качеств

        Args:
            url_openness (str): Полный путь к файлу с весами нейросетевой модели (открытость опыту)
            url_conscientiousness (str): Полный путь к файлу с весами нейросетевой модели (добросовестность)
            url_extraversion (str): Полный путь к файлу с весами нейросетевой модели (экстраверсия)
            url_agreeableness (str): Полный путь к файлу с весами нейросетевой модели (доброжелательность)
            url_neuroticism (str): Полный путь к файлу с весами нейросетевой модели (нейротизм)
            force_reload (bool): Принудительная загрузка файлов с весами нейросетевых моделей из сети
            out (bool): Отображение
            runtime (bool): Подсчет времени выполнения
            run (bool): Блокировка выполнения

        Returns:
            bool: **True** если веса нейросетевых моделей загружены, в обратном случае **False**
        """

        self._clear_notebook_history_output() # Очистка истории вывода сообщений в ячейке Jupyter

        try:
            # Проверка аргументов
            if (type(url_openness) is not str or not url_openness
                    or type(url_conscientiousness) is not str or not url_conscientiousness
                    or type(url_extraversion) is not str or not url_extraversion
                    or type(url_agreeableness) is not str or not url_agreeableness
                    or type(url_neuroticism) is not str or not url_neuroticism
                    or type(force_reload) is not bool
                    or type(out) is not bool
                    or type(runtime) is not bool or type(run) is not bool): raise TypeError
        except TypeError:
            self._inv_args(__class__.__name__, self.load_models_weights_b5.__name__, out = out); return False
        else:
            # Блокировка выполнения
            if run is False: self._error(self._lock_user, out = out); return False

            if runtime: self._r_start()

            result_download_models = 0 # Все веса нейросетевых моделей по умолчанию загружены

            # Информационное сообщение
            self._info(self._load_models_weights_b5, last = False, out = out)

            # Проход по всем URL с весами нейросетевых моделей
            for cnt, url in enumerate([
                (url_openness, self._b5['ru'][0]),
                (url_conscientiousness, self._b5['ru'][1]),
                (url_extraversion, self._b5['ru'][2]),
                (url_agreeableness, self._b5['ru'][3]),
                (url_neuroticism, self._b5['ru'][4]),
            ]):
                clear_output(True)
                sections = urlparse(url[0]) # Парсинг URL адреса

                try:
                    # URL файл невалидный
                    if sections.scheme == '': raise requests.exceptions.InvalidURL
                except requests.exceptions.InvalidURL:
                    url = os.path.normpath(url[0])

                    try:
                        if os.path.isfile(url) is False: raise FileNotFoundError # Не файл
                    except FileNotFoundError: self._other_error(self._load_model_weights_error, out = out); continue
                    except Exception: self._other_error(self._unknown_err, out = out); continue
                    else:
                        self._url_last_filename = url

                        # Отображение истории вывода сообщений в ячейке Jupyter
                        if out: self.show_notebook_history_output()
                else:
                    try:
                        # Загрузка файла из URL
                        res_download_file_from_url = self._download_file_from_url(
                            url = url[0], force_reload = force_reload, runtime = False, out = out, run = True
                        )
                    except Exception: self._other_error(self._unknown_err, out = out); continue
                    else:
                        # Файл загружен
                        if res_download_file_from_url != 200: continue

                        self._add_last_el_notebook_history_output(self._bold_wrapper(url[1].capitalize()))

                        result_download_models += 1

                        self._audio_models_b5[self._b5['en'][cnt]].load_weights(self._url_last_filename)

            clear_output(True)
            # Отображение истории вывода сообщений в ячейке Jupyter
            if out: self.show_notebook_history_output()

            if runtime: self._r_end(out = out)

            if result_download_models != len(self._b5['ru']): return False
            return True

    def get_acoustic_features(self, path: str, sr: int = 44100, window: Union[int, float] = 2.0,
                             step: Union[int, float] = 1.0, out: bool = True, runtime: bool = True, run: bool = True
                             ) -> Tuple[List[Union[np.ndarray, None]], List[Union[np.ndarray, None]]]:
        """Извлечение признаков из акустического сигнала (обертка)


        Args:
            path (str): Путь к аудио или видеофайлу
            sr (int): Частота дискретизации
            window (Union[int, float]): Размер окна сегмента сигнала (в секундах)
            step (Union[int, float]): Шаг сдвига окна сегмента сигнала (в секундах)
            out (bool): Отображение
            runtime (bool): Подсчет времени выполнения
            run (bool): Блокировка выполнения

        Returns:
            Tuple[List[Union[np.ndarray, None]], List[Union[np.ndarray, None]]]: Кортеж с двумя списками:

                1. Список с экспертными признаками
                2. Список с лог мел-спектрограммами
        """

        self._clear_notebook_history_output() # Очистка истории вывода сообщений в ячейке Jupyter

        return self._get_acoustic_features(path = path, sr = sr, window = window, step = step, last = False, out = out,
                                           runtime = runtime, run = run)

    def get_audio_union_predictions(self, depth: int = 1, recursive: bool = False, sr: int = 44100,
                                    window: Union[int, float] = 2.0, step: Union[int, float] = 1.0,
                                    out: bool = True, runtime: bool = True, run: bool = True) -> None:
        """Получения прогнозов по аудио

        Args:
            depth (int): Глубина иерархии для получения данных
            recursive (bool): Рекурсивный поиск данных
            sr (int): Частота дискретизации
            window (Union[int, float]): Размер окна сегмента сигнала (в секундах)
            step (Union[int, float]): Шаг сдвига окна сегмента сигнала (в секундах)
            out (bool): Отображение
            runtime (bool): Подсчет времени выполнения
            run (bool): Блокировка выполнения

        Returns:
            return None # TODO какой будет return?
        """

        self._clear_notebook_history_output() # Очистка истории вывода сообщений в ячейке Jupyter

        try:
            # Проверка аргументов
            if (type(depth) is not int or depth < 1 or type(out) is not bool or type(recursive) is not bool
                    or type(sr) is not int or sr < 1
                    or ((type(window) is not int or window < 1) and (type(window) is not float or window <= 0))
                    or ((type(step) is not int or step < 1) and (type(step) is not float or step <= 0))
                    or type(runtime) is not bool or type(run) is not bool):
                raise TypeError
        except TypeError:
            self._inv_args(__class__.__name__, self.get_audio_union_predictions.__name__, out = out); return None # TODO какой будет return?
        else:
            # Блокировка выполнения
            if run is False: self._error(self._lock_user, out = out); return None # TODO какой будет return?

            if runtime: self._r_start()

            try:
                # Получение директорий, где хранятся данные
                path_to_data = self._get_paths(self.path_to_dataset_, depth)
                if type(path_to_data) is bool: return None # TODO какой будет return?

                if type(self.keys_dataset_) is not list: raise TypeError

                # Словарь для DataFrame набора данных с данными
                self._dict_of_files = dict(zip(self.keys_dataset_, [[] for _ in range(0, len(self.keys_dataset_))]))
            except (TypeError, FileNotFoundError):
                self._other_error(self._folder_not_found.format(self._info_wrapper(self.path_to_dataset_)), out = out)
            except Exception: self._other_error(self._unknown_err, out = out); return None # TODO какой будет return?
            else:
                paths = [] # Пути до искомых файлов

                # Проход по всем директориям
                for curr_path in path_to_data:
                    empty = True # По умолчанию директория пустая

                    # Рекурсивный поиск данных
                    if recursive is True: g = Path(curr_path).rglob('*')
                    else: g = Path(curr_path).glob('*')

                    # Формирование словаря для DataFrame
                    for p in g:
                        try:
                            if type(self.ext_) is not list or len(self.ext_) < 1: raise TypeError

                            self.ext_ = [x.lower() for x in self.ext_]
                        except TypeError: self._other_error(self._som_ww, out = out); return None # TODO какой будет return?
                        except Exception: self._other_error(self._unknown_err, out = out); return None # TODO какой будет return?
                        else:
                            # Расширение файла соответствует расширению искомых файлов
                            if p.suffix.lower() in self.ext_:
                                if empty is True: empty = False # Каталог не пустой

                                paths.append(p.resolve())

                try:
                    self.__len_paths = len(paths) # Количество искомых файлов

                    if self.__len_paths == 0: raise TypeError
                except TypeError: self._other_error(self._files_not_found, out = out); return None # TODO какой будет return?
                except Exception: self._other_error(self._unknown_err, out = out); return None # TODO какой будет return?
                else:
                    # Локальный путь
                    self.__local_path = lambda path: os.path.join(
                        *Path(path).parts[-abs((len(Path(path).parts) - len(Path(self.path_to_dataset_).parts))):]
                    )

                    last = False # Замена последнего сообщения

                    # Проход по всем искомым файлов
                    for i, curr_path in enumerate(paths):
                        if i != 0: last = True

                        # Индикатор выполнения
                        self.__progressbar_union_predictions(
                            self._get_audio_union_predictions_info, i, self.__local_path(curr_path), last,
                            self.__len_paths, out
                        )

                        # Извлечение признаков из акустического сигнала
                        hc_features, melspectrogram_features = self._get_acoustic_features(
                            path = str(curr_path.resolve()),
                            sr = sr,
                            window = window,
                            step = step,
                            last = True, out = False, runtime = False, run = run
                        )

                        # Признаки из акустического сигнала извлечены
                        if len(hc_features) > 0 and len(melspectrogram_features) > 0:
                            # Коды ошибок нейросетевых моделей
                            code_error_pred_hc = -1
                            code_error_pred_melspectrogram = -1

                            try:
                                # Оправка экспертных признаков в нейросетевую модель
                                pred_hc = self.audio_model_hc_(np.array(hc_features, dtype = np.float16)).numpy()
                            except TypeError: code_error_pred_hc = 1
                            except Exception: code_error_pred_hc = 2

                            try:
                                # Отправка нейросетевых признаков в нейросетевую модель
                                pred_melspectrogram = self.audio_model_spec_(
                                    np.array(melspectrogram_features, dtype = np.float16)
                                ).numpy()
                            except TypeError: code_error_pred_melspectrogram = 1
                            except Exception: code_error_pred_melspectrogram = 2

                            if code_error_pred_hc != -1 and code_error_pred_melspectrogram != -1:
                                self._error(self._audio_models_not_formation, out = out); return None # TODO какой будет return?

                            if code_error_pred_hc != -1:
                                self._error(self._audio_model_hc_not_formation, out = out); return None # TODO какой будет return?

                            if code_error_pred_melspectrogram != -1:
                                self._error(self._audio_model_spec_not_formation, out = out); return None # TODO какой будет return?

                            # Конкатенация оценок по экспертным и нейросетевым признакам
                            union_pred = self.__concat_pred(pred_hc, pred_melspectrogram)

                            final_pred = []

                            for cnt, (name_b5, model) in enumerate(self.audio_models_b5_().items()):
                                result = model(np.expand_dims(union_pred[cnt], axis = 0)).numpy()[0][0]

                                final_pred.append(result)

                            # Добавление данных в словарь для DataFrame
                            if self._append_to_list_of_files(str(curr_path.resolve()), final_pred, out) is False:
                                return None # TODO какой будет return?
                        else:
                            pass # TODO
                    # Индикатор выполнения
                    self.__progressbar_union_predictions(
                        self._get_audio_union_predictions_info, self.__len_paths,
                        self.__local_path(paths[-1]), True, self.__len_paths, out
                    )

                    # Отображение в DataFrame с данными
                    self._df_files = pd.DataFrame.from_dict(data = self._dict_of_files, orient = 'index').transpose()
                    self._df_files.index.name = self._keys_id
                    self._df_files.index += 1

                    self._df_files.index = self._df_files.index.map(str)

                    # Отображение
                    if out is True:
                        self._add_notebook_history_output(self._df_files.iloc[0:self.num_to_df_display_, :])

                    clear_output(True)
                    # Отображение истории вывода сообщений в ячейке Jupyter
                    if out is True: self.show_notebook_history_output()
            finally:
                if runtime: self._r_end(out = out)