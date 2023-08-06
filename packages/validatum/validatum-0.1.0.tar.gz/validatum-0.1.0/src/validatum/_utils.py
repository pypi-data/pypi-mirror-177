#!/usr/bin/env python3

import string
import numpy as np
import pandas as pd
from itertools import combinations
from collections import defaultdict
from datetime import timedelta, datetime
from difflib import SequenceMatcher as SM


def simulate(
        size: int = 10_000, mistake: bool = False,
        error: float = 0.01, seed: int = 42) -> pd.DataFrame:
    np.random.seed(seed)
    inc1 = datetime.strptime('1/1/2018', '%d/%m/%Y')
    data = pd.DataFrame({
        'sex': np.random.choice(
            ['Female', 'Male', 'Unknown'],
            p=[0.49, 0.49, 0.02], size=size),
        'symptoms': np.random.choice(
            ['Chest pain', 'General Weakness', 'Abdominal pain', 'Falls'],
            p=[0.31, 0.29, 0.24, 0.16], size=size),
        'incident': [_randomDate(inc1, '365d') for i in range(size)],
    })
    data['DoB'] = data['incident'].apply(_randomDate, args=(f'-{365.25 * 80}D',))
    data['age'] = ((datetime.today() - data['DoB']) / pd.Timedelta('365.25D')).astype(int)
    data['arrival'] = data['incident'].apply(_randomDate, args=('4d',))
    data['registered'] = data['arrival'].apply(_randomDate, args=('4m',))
    data['departure'] = data['registered'].apply(_randomDate, args=('1d',))

    if mistake:
        for col in ['age']:
            data[col] = data[col].transform(_makeOutlier, error=error).astype(int)
        for col in ['sex', 'symptoms']:
            data[col] = data[col].apply(_spellMistake, error)
        for col in ['incident', 'arrival']:
            data[col] = data[col].apply(_dateMistake, error)

    return data


def _randomDate(start, delta='1Y'):
    """ Generate random date in range """
    if pd.isnull(start):
        return start
    if delta.startswith('-'):
        reverse = True
        delta = delta[1:]
    else:
        reverse = False
    delta = pd.Timedelta(delta)
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = np.random.randint(1, int_delta)
    delta = timedelta(seconds=random_second)
    if reverse:
        delta *= -1
    return start + delta


def _makeOutlier(x, error: float = 0.01):
    q1 = x.quantile(.25)
    q3 = x.quantile(.75)
    return x.apply(_setError, args=(q1, q3, error))


def _setError(x, q1, q3, error: float = 0.01):
    iqr = q3 - q1
    if np.random.random() < error:
        out = np.random.exponential(3)
        if np.random.random() < 0.5:
            return q1 - (out * iqr)
        else:
            return q3 + (out * iqr)
    else:
        return x


def _spellMistake(word, error: float = 0.01):
    if np.random.random() > error:
        return word
    idx = np.random.choice(range(len(word)))
    letter = word[idx]
    if letter.isupper():
        letters = string.ascii_uppercase
    else:
        letters = string.ascii_lowercase
    letters = [i for i in letters if i != letter]
    letter = np.random.choice(letters)
    return word[:idx] + letter + word[idx + 1:]


def _dateMistake(x, error: float = 0.01):
    units = ['year', 'month', 'day']
    unit = np.random.choice(units)
    p = [error / 2, 1 - error, error / 2]
    error = np.random.choice([-1, 0, 1], p=p)
    try:
        x = x.replace(**{unit: getattr(x, unit) + error})
    except ValueError:
        pass
    return x


def error_check(
        data: pd.DataFrame, error: float = 0.01, outlier: float = 3) -> dict:
    eventErrors = _getEventMisorder(data, error)
    numericOutliers = _getNumericOutliers(data, outlier)
    spellingErrors = _getMispelling(data, error)
    return {**eventErrors, **numericOutliers, **spellingErrors}


def _estimateDependence(data: pd.DataFrame, error: float = 0.01):
    """ Find pairs of datetime columns
        with consistent order of event"""
    dependence = []
    timeData = data.select_dtypes(include=['datetime64'])
    for t1, t2 in combinations(timeData.columns, 2):
        sub = data[[t1, t2]].dropna()
        ratio = (sub[t1] > sub[t2]).mean()
        if ratio < error:
            dependence.append((t1, t2))
        elif ratio > 1 - error:
            dependence.append((t2, t1))
    return dependence


def _getEventMisorder(
        data: pd.DataFrame, error: float = 0.01,
        equal: bool = True):
    dependence = _estimateDependence(data, error)
    errors = defaultdict(list)
    for t1, t2 in dependence:
        if equal:
            idxs = data.loc[data[t1] >= data[t2]].index
        else:
            idxs = data.loc[data[t1] > data[t2]].index
        if idxs.empty:
            continue
        msg = f'Misordered event: "{t1}" after "{t2}"'
        for idx in idxs:
            errors[idx].append(msg)
    return dict(errors)


def _assessOutlier(x):
    q1 = x.quantile(.25)
    q2 = x.quantile(.50)
    q3 = x.quantile(.75)
    return x.apply(_getIQRthreshold, args=(q1, q2, q3))


def _getIQRthreshold(x, q1, q2, q3):
    """ Compute outlier threshold """
    iqr = q3 - q1
    if q1 <= x < q3:
        return 0
    elif x > q2:
        return (x - q3) / iqr
    else:
        return -((q1 - x) / iqr)


def _getNumericOutliers(data: pd.DataFrame, threshold: float = 3):
    numericData = data.select_dtypes(include=['number'])
    errors = defaultdict(list)
    for col in numericData.columns:
        scaled = data[col].transform(_assessOutlier)
        for idx, outlier in scaled.items():
            if abs(outlier) < threshold:
                continue
            val = data.loc[data.index == idx, col].values[0]
            msg = f'Outlier in "{col}": '
            if outlier < 0:
                msg += f'{val} < Q1 - (IQR * {abs(outlier):.2f})'
            else:
                msg += f'{val} > Q3 + (IQR * {outlier:.2f})'
            errors[idx].append(msg)
    return dict(errors)


def _assessMispelling(
        col: pd.Series, error: float = 0.01, distance: float = 0.75):
    words = col.value_counts().reset_index().apply(tuple, axis=1)
    words = combinations(words, 2)
    misspelling = []
    for (w1, c1), (w2, c2) in words:
        if SM(None, w1, w2).ratio() < distance:
            continue
        ratio = c1 / (c1 + c2)
        if ratio < error:
            misspelling.append((w1, w2))
        elif ratio > 1 - error:
            misspelling.append((w2, w1))
    return misspelling


def _getMispelling(
        data: pd.DataFrame, error: float = 0.01,
        distance: float = 0.75):
    errors = defaultdict(list)
    strData = data.select_dtypes(include=['object'])
    for col in strData.columns:
        misspelling = _assessMispelling(data[col])
        for mispelled, ref in misspelling:
            idxs = data.loc[data[col] == mispelled].index
            msg = f'Mispelling in "{col}": ("{mispelled}" -> "{ref}")'
            for idx in idxs:
                errors[idx].append(msg)
    return dict(errors)
