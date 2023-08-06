# -*- coding: utf-8 -*-
from sf_etl_py3._Sfconfig import _SfQyConfig, _SfQyParConfig
from sf_etl_py3.SfQyModule import wave


class SfQy:
    def __init__(self, **kwargs):
        self.qy_config = _SfQyConfig(**kwargs)
        self.qy_par_config = _SfQyParConfig(**self.qy_config.parameter_dict)
        # self.par_config = _ParameterConfig(self.qy_config.parameter_dict) if self.qy_config.parameter_dict else None

    def start(self):
        """
        :return: dict
        """
        result_dict = dict()
        if self.qy_config.monitor_type == 'zzzz':
            pass
        if self.qy_config.monitor_type == '准确性':
            """
            : 以表为单位, 指标的波动率检查
            """
            result_dict = wave.wave(self.qy_config, self.qy_par_config)

        return result_dict

