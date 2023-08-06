# -*- encoding:utf-8 -*-
import numpy as np
import pandas as pd


def annchg(spots, futures, interval, drift=None, offset=None, **kwargs):
    offset = int(offset) if isinstance(offset, int) else 0
    drift = int(drift) if isinstance(drift, int) else 365.0

    annchg = ((spots - futures) / futures) * drift / interval

    # Offset
    if offset != 0:
        annchg = annchg.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        annchg.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        annchg.fillna(method=kwargs["fill_method"], inplace=True)
    return annchg


def rsannchg(spots, recent, srinterval, drift=None, offset=None, **kwargs):
    return annchg(spots=spots,
                  futures=recent,
                  interval=srinterval,
                  drift=drift,
                  offset=offset,
                  **kwargs)


def msannchg(spots, main, sminterval, drift=None, offset=None, **kwargs):
    return annchg(spots=spots,
                  futures=main,
                  interval=sminterval,
                  drift=drift,
                  offset=offset,
                  **kwargs)


def fsannchg(spots, far, sfinterval, drift=None, offset=None, **kwargs):
    return annchg(spots=spots,
                  futures=far,
                  interval=sfinterval,
                  drift=drift,
                  offset=offset,
                  **kwargs)


def ssannchg(spots, second, ssinterval, drift=None, offset=None, **kwargs):
    return annchg(spots=spots,
                  futures=second,
                  interval=ssinterval,
                  drift=drift,
                  offset=offset,
                  **kwargs)