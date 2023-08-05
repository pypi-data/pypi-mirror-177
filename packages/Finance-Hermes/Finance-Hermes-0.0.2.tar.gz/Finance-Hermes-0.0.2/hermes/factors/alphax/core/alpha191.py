# -*- encoding:utf-8 -*-
import numpy as np
from hermes.factors.technical.factor_overlap import *
from hermes.factors.technical.factor_statistics import *


def alpha191_2(close, low, high, offset=None, **kwargs):
    ###-1 * delta(((T1-T2)/((high-low)),1))
    offset = int(offset) if isinstance(offset, int) else 0
    # Calculate Result
    diff = ((close - low) - (high - close)) / (high - low)
    alpha2 = diff - diff.shift(1)

    # Offset
    if offset != 0:
        alpha2 = alpha2.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        alpha2.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        alpha2.fillna(method=kwargs["fill_method"], inplace=True)

    return alpha2


def alpha191_6(open, high, length=None, offset=None, **kwargs):
    # (RANK(SIGN(DELTA((((OPEN0*85)+(HIGH0*15))),4)))*-1)
    length = int(length) if length and length > 0 else 4
    offset = int(offset) if isinstance(offset, int) else 0
    diff = (open * 0.85 + high * 0.15)
    alpha6 = np.sign((diff - diff.shift(4)))

    # Offset
    if offset != 0:
        alpha6 = alpha6.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        alpha6.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        alpha6.fillna(method=kwargs["fill_method"], inplace=True)

    return alpha6


def alpha191_14(close, length=None, offset=None, **kwargs):
    length = int(length) if length and length > 0 else 5
    offset = int(offset) if isinstance(offset, int) else 0

    alpha14 = close - close.shift(length)

    # Offset
    if offset != 0:
        alpha14 = alpha14.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        alpha14.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        alpha14.fillna(method=kwargs["fill_method"], inplace=True)

    return alpha14


def alpha191_15(close, open, length=None, offset=None, **kwargs):
    length = int(length) if length and length > 0 else 5
    offset = int(offset) if isinstance(offset, int) else 0

    alpha15 = open / close.shift(1)

    # Offset
    if offset != 0:
        alpha15 = alpha15.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        alpha15.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        alpha15.fillna(method=kwargs["fill_method"], inplace=True)

    return alpha15


def alpha191_18(close, length=None, offset=None, **kwargs):
    length = int(length) if length and length > 0 else 5
    offset = int(offset) if isinstance(offset, int) else 0

    alpha18 = close - close.shift(5)

    # Offset
    if offset != 0:
        alpha18 = alpha18.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        alpha18.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        alpha18.fillna(method=kwargs["fill_method"], inplace=True)

    return alpha18


def alpha191_20(close, length=None, offset=None, **kwargs):
    length = int(length) if length and length > 0 else 6
    offset = int(offset) if isinstance(offset, int) else 0

    alpha20 = (close - close.shift(length)) / close.shift(length)

    # Offset
    if offset != 0:
        alpha20 = alpha20.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        alpha20.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        alpha20.fillna(method=kwargs["fill_method"], inplace=True)

    return alpha20


def alpha191_24(close, length=None, offset=None, **kwargs):
    length = int(length) if length and length > 0 else 5
    offset = int(offset) if isinstance(offset, int) else 0

    alpha24 = sma(close=close - close.shift(length), length=length, **kwargs)

    # Offset
    if offset != 0:
        alpha24 = alpha24.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        alpha24.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        alpha24.fillna(method=kwargs["fill_method"], inplace=True)

    return alpha24


def alpha191_27(close, offset=None, **kwargs):
    offset = int(offset) if isinstance(offset, int) else 0

    # (CLOSE[0] - CLOSE[3]) / CLOSE[3] * 100 + (CLOSE[0] - CLOSE[6]) / CLOSE[6] * 100
    alpha27 = (close - close.shift(3)) / close.shift(3) + (
        close - close.shift(6)) / close.shift(6)

    # Offset
    if offset != 0:
        alpha27 = alpha27.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        alpha27.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        alpha27.fillna(method=kwargs["fill_method"], inplace=True)

    return alpha27


def alpha191_29(close, volume, length=None, offset=None, **kwargs):
    length = length if length and length > 0 else 6
    offset = int(offset) if isinstance(offset, int) else 0

    min_periods = int(
        kwargs["min_periods"]) if "min_periods" in kwargs and kwargs[
            "min_periods"] is not None else length

    alpha29 = (close - close.shift(6)
               ) / close.shift(6) * volume / volume.rolling(length).mean()

    # Offset
    if offset != 0:
        alpha29 = alpha29.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        alpha29.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        alpha29.fillna(method=kwargs["fill_method"], inplace=True)

    return alpha29


def alpha191_32(close, high, volume, length=None, offset=None, **kwargs):
    length = length if length and length > 0 else 3
    min_periods = int(
        kwargs["min_periods"]) if "min_periods" in kwargs and kwargs[
            "min_periods"] is not None else length

    offset = int(offset) if isinstance(offset, int) else 0

    a = volume - volume.rolling(length).mean()
    b = high / close
    c = a.rank(axis=1)
    d = b.rank(axis=1)
    e = c.rolling(length).corr(d)
    f = e.rank(axis=1)
    alpha32 = f.rolling(length).sum()

    # Offset
    if offset != 0:
        alpha32 = alpha32.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        alpha32.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        alpha32.fillna(method=kwargs["fill_method"], inplace=True)

    return alpha32


def alpha191_34(close, length=None, offset=None, **kwargs):
    length = length if length and length > 0 else 12
    min_periods = int(
        kwargs["min_periods"]) if "min_periods" in kwargs and kwargs[
            "min_periods"] is not None else length

    offset = int(offset) if isinstance(offset, int) else 0

    alpha34 = close.rolling(length).mean() / close

    # Offset
    if offset != 0:
        alpha34 = alpha34.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        alpha34.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        alpha34.fillna(method=kwargs["fill_method"], inplace=True)

    return alpha34


def alpha191_42(close, high, volume, length=None, offset=None, **kwargs):
    length = length if length and length > 0 else 10
    min_periods = int(
        kwargs["min_periods"]) if "min_periods" in kwargs and kwargs[
            "min_periods"] is not None else length

    offset = int(offset) if isinstance(offset, int) else 0
    b = stdev(high / close, length=10)
    c = high.rolling(length).corr(volume)
    alpha42 = -1 * b.rank(axis=1) * c

    # Offset
    if offset != 0:
        alpha42 = alpha42.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        alpha42.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        alpha42.fillna(method=kwargs["fill_method"], inplace=True)

    return alpha42


def alpha191_46(close, length=None, offset=None, **kwargs):
    length = length if length and length > 0 else 3
    offset = int(offset) if isinstance(offset, int) else 0
    a = close.rolling(length).mean()
    b = close.rolling(length * 2).mean()
    c = close.rolling(length * 4).mean()
    e = close.rolling(length * 12).mean()

    alpha46 = (a + b + c + e) / (4 * close)

    # Offset
    if offset != 0:
        alpha46 = alpha46.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        alpha46.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        alpha46.fillna(method=kwargs["fill_method"], inplace=True)

    return alpha46


def alpha191_47(close, high, low, length=None, offset=None, **kwargs):
    length = length if length and length > 0 else 6
    min_periods = int(
        kwargs["min_periods"]) if "min_periods" in kwargs and kwargs[
            "min_periods"] is not None else length

    offset = int(offset) if isinstance(offset, int) else 0

    alpha47 = (high.rolling(length).max() - close) / (
        high.rolling(length).max() - low.rolling(length).min())

    # Offset
    if offset != 0:
        alpha47 = alpha47.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        alpha47.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        alpha47.fillna(method=kwargs["fill_method"], inplace=True)

    return alpha47