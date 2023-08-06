# -*- coding: utf-8 -*-
import ast


class _SfQyConfig:
    """
    参数
    """
    def __init__(self,
                 task_name=None,
                 source_data=None,
                 source_config_dict=None,
                 compare_data=None,
                 compare_config_dict=None,
                 monitor_type=None,
                 parameter_dict=None,
                 feedback_code=None,
                 msg_bot=None,
                 bot_list=None,
                 ):
        # 任务名
        self.task_name = task_name
        # 数据源,是一个sql或者表名或者视图
        self.source_data = source_data
        self.source_config_dict = dict() if source_config_dict is None else source_config_dict
        # 监控类别: 完整性\准确性\一致性\及时性
        self.monitor_type = monitor_type
        # TODO 比较的源 行数据 ，用来和source_data做对比, 此版本不上
        self.compare_data = compare_data
        self.compare_config_dict = dict() if compare_config_dict is None else compare_config_dict
        # 参数列表
        self.parameter_dict = dict() if parameter_dict is None else parameter_dict
        # -------- 反馈码 --------
        # 100000 返回全部消息
        # 100100 返回符合条件的消息
        self.feedback_code = feedback_code
        # 机器人
        self.msg_bot = msg_bot
        self.bot_list = list() if bot_list is None else bot_list

        # 参数检查
        self._check()

    def _check(self):
        if isinstance(self.source_config_dict, str):
            self.source_config_dict = ast.literal_eval(self.source_config_dict)
        if not isinstance(self.source_config_dict, dict) or not self.source_config_dict:
            raise ValueError('source_config_dict is not dict')

        if isinstance(self.compare_config_dict, str):
            self.compare_config_dict = ast.literal_eval(self.compare_config_dict)
        if not isinstance(self.compare_config_dict, dict):
            raise ValueError('compare_config_dict is not dict')

        if isinstance(self.parameter_dict, str):
            self.parameter_dict = ast.literal_eval(self.parameter_dict)
        if not isinstance(self.parameter_dict, dict):
            raise ValueError('parameter_dict is not dict')

        if not isinstance(self.bot_list, list):
            raise ValueError('bot_list is not dict')


class _SfQyParConfig:
    """
    参数
    """
    def __init__(self,
                 dim_list=None,
                 mea_dict=None,
                 mea_dict_list=None,
                 comparison_list=None,
                 comparison_where=None,
                 ):
        # 波动范围
        # self.mea_range = mea_range
        # self.mea_max = mea_max
        # self.mea_min = mea_min

        # 维度列表
        self.dim_list = list() if dim_list is None else dim_list
        # ---------------- 指标列表 ----------------
        #  [{'mea_name': 'install_cnt', 'monitor_method': '波动率', 'mea_range': '[-0.3, 0.3]', 'poly_type': 'sum'}]
        self.mea_dict = dict() if mea_dict is None else mea_dict
        # ['install_cnt', reg_cnt]
        self.mea_list = list()

        # 指标列表
        self.mea_dict_list = list() if mea_dict_list is None else mea_dict_list
        # 阶段字段组合
        self.comparison_list = list() if comparison_list is None else comparison_list

        self.comparison_where = comparison_where
        self._check()

    def _check(self):
        # ---------- 检查类型 -----------
        if not isinstance(self.mea_list, list):
            raise ValueError('mea_list is not list')
        if not isinstance(self.mea_dict_list, list):
            raise ValueError('mea_dict_list is not list')

        # ---------- 格式和默认值 -----------
        temp_diff_list = list()
        for mea_dict in self.mea_dict_list:
            if not {'mea_name', 'monitor_method', 'mea_range'}.issubset(set(mea_dict.keys())):
                raise ValueError('mea_dict need key [mea_name and monitor_method and mea_range]')
            else:
                if mea_dict.get('mea_name') not in self.mea_list:
                    self.mea_list.append(mea_dict.get('mea_name'))

            mea_name = mea_dict.get('mea_name')
            monitor_method = mea_dict.get('monitor_method')
            poly_type = mea_dict.get('poly_type') if mea_dict.get('poly_type') else 'sum'
            diff_key = ('%s -- %s -- %s' % (mea_name, monitor_method, poly_type))
            if diff_key in temp_diff_list:
                raise ValueError('mea_dict_list: No duplicate data of '
                                 'mea_name, monitor_method and poly_type in mea_dict_list')
        # ---------- 值规范检查 -----------


# class _ReadMe:
#     """
#     100
#     """
#     def __init__(self):
#         pass
#
#     @staticmethod
#     def feedback_code(v):
#         """
#         100000 返回全部消息
#         100100 有符合规则才返回消息
#         100200
#         """
#         return v
