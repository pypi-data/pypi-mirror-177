# -*- coding: utf-8 -*-
from sf_etl_py3._Sfconfig import _SfQyConfig, _SfQyParConfig
from sf_etl_py3.SfQyModule import wave, customize_sql
from sf_etl_py3.Bot import DingBot
from sf_etl_py3.Utils import pg_fetchall, pg_execute
from sf_etl_py3._SfSql import _QyPgSql
import json


class SfQy:
    def __init__(self, **kwargs):
        self.qy_config = _SfQyConfig(**kwargs)
        self.qy_par_config = _SfQyParConfig(**self.qy_config.parameter_dict)
        # self.par_config = _ParameterConfig(self.qy_config.parameter_dict) if self.qy_config.parameter_dict else None

    def _check(self):
        # --------- 初始化检查 ---------

        # 检查配置表, 不存在则创建
        config_table_name = self.qy_config.config_table_name
        schema_name = self.qy_config.config_table_name.split('.')[0]
        table_name = self.qy_config.config_table_name.split('.')[1]
        rows = pg_fetchall(self.qy_config.source_config_dict, _QyPgSql.SfQyPgExistsTableSql.
                           format(schema_name=schema_name, table_name=table_name))
        if rows[0].get('cnt') == 0:
            pg_execute(self.qy_config.source_config_dict, _QyPgSql.SfQyPgCreateQualityConfigSql.
                       format(table_name=config_table_name))

        # 检查日期表, 不存在则创建
        config_table_name = self.qy_config.log_table_name
        schema_name = self.qy_config.log_table_name.split('.')[0]
        table_name = self.qy_config.log_table_name.split('.')[1]
        rows = pg_fetchall(self.qy_config.source_config_dict, _QyPgSql.SfQyPgExistsTableSql.
                           format(schema_name=schema_name, table_name=table_name))
        if rows[0].get('cnt') == 0:
            pg_execute(self.qy_config.source_config_dict, _QyPgSql.SfQyPgCreateQualityLogSql.
                       format(table_name=config_table_name))

    def start(self):
        """
        :return: dict
            * monitor_type: str 类别
            * task_name: str 任务名
            * data: dict 返回数据
        """
        # ------ 依赖检查 ------
        self._check()
        # ------ 返回的字段 ------
        result_dict = dict()

        # ------ 区分流程：自定义sql ------
        if self.qy_config.monitor_type == '自定义sql':
            result_dict = customize_sql.customize_sql(self.qy_config, self.qy_par_config)

        # ------ 区分流程：指标波动 ------
        if self.qy_config.monitor_type == '准确性':
            """
            : 以表为单位, 指标的波动率检查
            """
            result_dict = wave.wave(self.qy_config, self.qy_par_config)
        self.feedback(result_dict)
        return result_dict

    def feedback(self, result_dict: dict):
        ding_obj = DingBot()
        task_name = result_dict.get('task_name')
        data_list = result_dict.get('data')
        bot_dict_list = self.qy_config.bot_dict_list

        if result_dict.get('monitor_type') == '自定义sql':
            msg_list = list()
            msg_list.append('【 %s 】 ' % task_name)

            for data_dict in data_list:
                result_data = data_dict.get('result_data')
                abnormal_condition = self.qy_par_config.abnormal_condition
                true_or_false = eval('result_data %s' % abnormal_condition)
                if true_or_false:
                    msg_list.append('自定义sql异常,数据为: %s\n\n' % result_data)
                else:
                    msg_list.append('指标符合预期\n\n')
            for bot_dict in bot_dict_list:
                bot_url = bot_dict.get('bot_url')
                bot_sec = bot_dict.get('bot_sec')
                level = bot_dict.get('level')
                if level == 1 and bot_url:
                    ding_obj.set_kwargs(url=bot_url, sec=bot_sec)
                    ding_obj.send_text('\n'.join(msg_list))

        if result_dict.get('monitor_type') == '准确性':
            except_num = 0  # 异常指标个数
            msg_list = list()
            msg_list.append('【 %s 】 ' % task_name)
            for i in data_list:
                if i.get('is_except') == 1:
                    except_num += 1
                    # ------ 取出参数 ------
                    dim_dict = i.get('dim')
                    mea_name = i.get('mea_name')
                    monitor_method = i.get('monitor_method')
                    curr_value = i.get('curr_value')
                    diff_value = i.get('diff_value')
                    diff_result = i.get('diff_result')
                    expect_value = i.get('expect_value')

                    msg_list.append('指标[%s]异常: %s' % (monitor_method, mea_name))
                    if dim_dict:
                        dim_str_list = list()
                        for k, v in dim_dict.items():
                            dim_str_list.append("%s[%s]" % (k, v))
                        msg_list.append('维度: %s' % ','.join(dim_str_list))
                    msg_list.append('当前[%s] 和 [%s]比较' % (curr_value, diff_value))
                    msg_list.append('波动为: %s' % diff_result)
                    msg_list.append('期望为: %s\n' % expect_value)
            if except_num == 0:
                msg_list.append('指标均符合规范')

            for bot_dict in bot_dict_list:
                bot_url = bot_dict.get('bot_url')
                bot_sec = bot_dict.get('bot_sec')
                level = bot_dict.get('level')
                if level == 1 and bot_url:
                    ding_obj.set_kwargs(url=bot_url, sec=bot_sec)
                    ding_obj.send_text('\n'.join(msg_list))



