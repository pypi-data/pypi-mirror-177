# -*- encoding:utf-8 -*-
from hermes.factors.base import FactorBase, LongCallMixin, ShortMixin
from hermes.factors.fundamentals.core.basis import *


class FactorBasis(FactorBase, LongCallMixin, ShortMixin):

    def __init__(self, **kwargs):
        __str__ = 'basis'
        self.category = 'basis'

    def _init_self(self, **kwargs):
        pass

    def RSACHG(self,
               data,
               drift=None,
               offset=None,
               dependencies=['spots', 'recent', 'srinterval'],
               **kwargs):
        result = rsannchg(data['spots'],
                          data['recent'],
                          data['srinterval'],
                          drift=drift,
                          offset=offset,
                          **kwargs)
        return self._format(result, f"RSACHG")

    def MSACHG(self,
               data,
               drift=None,
               offset=None,
               dependencies=['spots', 'main', 'sminterval'],
               **kwargs):
        result = msannchg(data['spots'],
                          data['main'],
                          data['sminterval'],
                          drift=drift,
                          offset=offset,
                          **kwargs)
        return self._format(result, f"MSACHG")

    def SSACHG(self,
               data,
               drift=None,
               offset=None,
               dependencies=['spots', 'second', 'ssinterval'],
               **kwargs):
        result = ssannchg(data['spots'],
                          data['second'],
                          data['ssinterval'],
                          drift=drift,
                          offset=offset,
                          **kwargs)
        return self._format(result, f"SSACHG")

    def FSACHG(self,
               data,
               drift=None,
               offset=None,
               dependencies=['spots', 'far', 'sfinterval'],
               **kwargs):
        result = fsannchg(data['spots'],
                          data['far'],
                          data['sfinterval'],
                          drift=drift,
                          offset=offset,
                          **kwargs)
        return self._format(result, f"FSACHG")
