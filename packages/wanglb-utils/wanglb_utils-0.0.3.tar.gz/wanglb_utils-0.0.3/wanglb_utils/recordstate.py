# -*- coding:utf-8 -*-
# @FileName :recordstate.py
# @DateTime :2022/3/31 10:25
# @Author   :wanglb
# 需要Mongodb数据库的支持
from datetime import datetime, date
import yaml
import sys
import os

try:
    from pymongo import MongoClient
except:
    pass

"""
mongo 操作符
$lt		小于
$gt		大于
$lte	小于等于
$regex	正则
$in		包含
$size	元素数量
"""


class RecordState(object):
    """
    作为状态记录的基类
    动作状态可以继承，也可以初始化写
    """
    def __init__(self, class_name=''):
        self._base_class_name = 'RecordState'
        self.class_name = class_name or self.__subclass_name()
        self._state_base = dict()
        self._state_this = dict()
        self._base_dir = ''
        self.__init_dir()
        self._this_file = os.path.join(self._base_dir, self.class_name + '.yml')
        self._base_file = os.path.join(self._base_dir, self._base_class_name + '.yml')
        self.__read_base_file()
        self.__read_this_file()

    def __init_dir(self):
        self._base_dir = self.__get_site() + r'\auto_state'
        if not os.path.exists(self._base_dir):
            os.mkdir(self._base_dir)

    def __read_this_file(self):
        if os.path.isfile(self._this_file):
            with open(self._this_file, 'r', encoding='utf-8') as f:
                self._state_this = yaml.full_load(f)

    def __read_base_file(self):
        if os.path.isfile(self._base_file):
            with open(self._base_file, 'r', encoding='utf-8') as f:
                self._state_base = yaml.full_load(f)

    def __save_this_file(self):
        with open(self._this_file, 'w+', encoding='utf-8') as f:
            yaml.dump(self._state_this, f)

    def __save_base_file(self):
        with open(self._base_file, 'w+', encoding='utf-8') as f:
            yaml.dump(self._state_base, f)

    @classmethod
    def __subclass_name(cls):
        # 返回子类的类名
        return cls.__name__

    @staticmethod
    def __get_site():
        frame = sys._getframe()
        filename = frame.f_code.co_filename
        return os.path.dirname(filename)

    def read_state(self, key, default):
        """
        读取动作状态
        :param key: 变量名
        :param default: 不存在时，默认值
        :return: 返回对应变量名的结果
        """
        return self._state_this.get(key, default)

    def write_state(self, key, value):
        """
        写入动作状态
        :param key: 变量名
        :param value: 变量内容
        :return: None
        """
        self._state_this[key] = value
        self.__save_this_file()

    def read_base_state(self, key, default):
        """
        读取全局状态
        :param key: 变量名
        :param default: 不存在时，默认值
        :return: 返回对应变量名的结果
        """
        return self._state_base.get(key, default)

    def write_base_state(self, key, value):
        """
        写入全局状态
        :param key: 变量名
        :param value: 不存在时，默认值
        :return: None
        """
        self._state_base[key] = value
        self.__save_base_file()


class LogRecord(object):
    """
    程序运行日志记录部分，记录在mongodb数据库中
    """
    def __init__(self, collect_name=''):
        collect_name = collect_name or 'other'
        client = MongoClient('mongodb://localhost:27017/')
        db = client['local_log_record']
        self.__collect = db[collect_name]

    @staticmethod
    def __to_log(msg, time_show=True, end='\n'):
        if time_show:
            current_time = datetime.now().strftime('%m-%d %H:%M:%S')
            msg_in = f'{current_time} -> {msg}'
        else:
            msg_in = f'{msg}'
        print(msg_in, end=end)

    def record(self, dic):
        if '_record_time' not in dic:
            _record_time = datetime.now()
            dic['_record_time'] = _record_time
        dic['run_date'] = datetime.strptime(str(date.today()), '%Y-%m-%d')
        try:
            self.__collect.insert_one(dic)
        except Exception as e:
            self.__to_log(f'日志记录出错\n{e}')

    def query_all(self, arg=None, project=None):
        if not project:
            project = {}
        if '_id' not in project:
            project['_id'] = 0
        if arg and isinstance(arg, dict):
            data = list(self.__collect.find(arg, projection=project))
        else:
            data = list(self.__collect.find(projection=project))
        return data


class LogOutput(object):
    def __init__(self, module='Test'):
        try:
            self.record = LogRecord(module)
        except:
            self.record = None

    @staticmethod
    def to_log(msg, time_show=True, end='\n', ):
        if time_show:
            dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            msg = f'{dt} -> {msg}'
        print(msg, end=end)

    def record_log(self, txt, body=None, _type='info'):
        if not self.record:
            self.to_log('没有MongoDB，无法记录相关日志')
            return
        if not body:
            body = ''
        self.record.record({'content': {'text': txt, 'body': body}, 'type': _type})
