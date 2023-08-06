# -*- coding:utf-8 -*-
# @FileName : utils_func.py
# @DateTime : 2022/11/16 17:34
# @Author   : wanglb
from threading import Thread, Condition, Lock
from datetime import datetime, timedelta
from typing import Iterable
import threading
import requests
import platform
import socket
import json
import re
import os


IS_LOCAL = platform.system() == 'Windows'
thread_max = threading.BoundedSemaphore(10)
semaphore = threading.Semaphore(3)


class Event:
    def __init__(self):
        self._cond = Condition(Lock())
        self._flag = False

    def _reset_internal_locks(self):
        self._cond.__init__(Lock())

    def is_set(self):
        return self._flag

    isSet = is_set

    def set(self):
        with self._cond:
            self._flag = True
            self._cond.notify_all()

    def clear(self):
        with self._cond:
            self._flag = False

    def wait(self, timeout=None):
        with self._cond:
            signaled = self._flag
            if not signaled:
                signaled = self._cond.wait(timeout)
            return signaled


class WaitThread(Thread):
    def __init__(self, interval, func, *args):
        super().__init__()
        self.interval = interval
        self.func = func
        self.args = args
        self.finish = Event()
        self.setDaemon(True)

    def cancel(self):
        self.finish.set()

    def reset(self):
        self.finish.set()
        self.run()

    def run(self):
        self.finish.wait(self.interval)
        if not self.finish.is_set():
            self.func(*self.args)
        self.finish.set()


class StartThread(threading.Thread):
    def __init__(self, func, args=None):
        threading.Thread.__init__(self)
        self.func = func
        self.args = args

    def run(self):
        if self.args:
            self.func(self.args)
        else:
            self.func()
        thread_max.release()


def multi_thread(func, lis: list):
    thread_list = []
    for each in lis:
        thread_max.acquire()
        m = StartThread(func, each)
        m.start()
        thread_list.append(m)
    for m in thread_list:
        m.join()


def start_new_thread(func, args=(), name=None):
    task = threading.Thread(target=func, args=args, name=name)
    task.setDaemon(True)
    task.start()


def search(content, lis: list, case: bool = True, index: int = 0):
    """
    二分法查找
    :param content: 要找的内容
    :param lis: 在哪里找
    :param case: 是否精确查找
    :param index: 从第几个开始找
    :return:
    """
    lis.sort()
    mid = len(lis) // 2
    if len(lis) == 1:
        if content != lis[0]:
            if case:
                return -1
            else:
                return index
        else:
            return index
    if content == lis[mid]:
        return mid
    elif content < lis[mid]:
        return search(content, lis[:mid], case, index)
    else:
        return search(content, lis[mid:], case, index + mid)


def expand(lis, none: [None, str] = None):
    """
    多层迭代对象展开，字符串不展开
    params lis: 原始的迭代对象
    params none: 遇到None的处理方式，‘exclude’ 跳过；None 保持不变；其他字符串 替换为对应的字符串
    """
    ll = []
    for each in lis:
        if isinstance(each, Iterable) and not isinstance(each, str):
            ll.extend(expand(each))
        else:
            if each is None:
                each = none
            if each != 'exclude':
                ll.append(each)
    return ll


def time_format(r_time):
    """
    字符串的時間格式轉換為真正的日期時間格式
    :param r_time: 字符串日期时间格式
    :return:
    """
    r_time = r_time.strip()
    now_time = datetime.now()
    rr_time = ''
    dt = tm = ''
    if _dt := re.findall(r'\d+年\d+月\d+日', r_time):
        dt = datetime.strptime(_dt[0], '%Y年%m月%d日').strftime('%Y-%m-%d')
    if _tm := re.findall(r'\d+:\d+:\d+', r_time):
        tm = datetime.strptime(_tm[0], '%H:%M:%S').strftime('%H:%M:%S')
    elif _tm := re.findall(r'\d+:\d+', r_time):
        tm = datetime.strptime(_tm[0], '%H:%M').strftime('%H:%M:%S')
    if tm:
        if not dt:
            dt = datetime.today().strftime('%Y-%m-%d')
        return datetime.strptime(dt + ' ' + tm, '%Y-%m-%d %H:%M:%S')
    if '周' in r_time or '星期' in r_time:
        try:
            r_time = r_time.replace('星期', '周')
            r_time = now_time - timedelta(weeks=int(r_time.split('周')[0].strip()))
        except:
            rr_time = r_time
    elif '天' in r_time and '昨天' not in r_time:
        try:
            r_time = now_time - timedelta(days=int(r_time.split('天')[0].strip()))
        except:
            rr_time = r_time
    elif '小時' in r_time:
        try:
            r_time = now_time - timedelta(hours=int(r_time.split('小時')[0].strip()))
        except:
            rr_time = r_time
    elif '分鐘' in r_time:
        try:
            r_time = now_time - timedelta(minutes=int(r_time.split('分鐘')[0].strip()))
        except:
            rr_time = r_time
    elif '剛剛' in r_time:
        r_time = now_time
    elif '發佈' in r_time:
        li = r_time.split(' ')
        if li[0] == '昨天':
            try:
                rr_time = (datetime.now() - timedelta(days=1)).strftime('%Y/%m/%d ') + li[1]
                rr_time = datetime.strptime(rr_time, '%Y/%m/%d %H:%M')
            except:
                rr_time = r_time
    elif '月' in r_time and '日' in r_time:
        r_t = f'{now_time.year}年{r_time} 00:00'
        try:
            rr_t = re.findall(r'\d{4}年\d{1,2}月\d{1,2}日 \d{1,2}:\d{1,2}', r_t)
            rr_time = datetime.strptime(rr_t[0], '%Y年%m月%d日 %H:%M')
        except:
            rr_time = r_time
    else:
        rr_time = r_time
    if not rr_time:
        rr_time = r_time
    return rr_time


def clear_character(st):
    """
    清除无效字符串
    :param st: 原始字符串
    :return:
    """
    comp = re.compile(r'[\u4e00-\u9fa50-9a-zA-Z~!@#$%^&*()_+=\-\\|:：；‘”“’";\'\[\]{}/\n.,，。？? ！`—【】「」『』]+')
    st = ''.join(comp.findall(st))
    return st


def func_st_datetime(x):
    """
    转换为日期时间格式，一般在pandas处理数据使用
    :param x: 日期时间格式，可能会有错误值
    :return:
    """
    try:
        return x.strftime('%Y-%m-%d %H:%M:%S')
    except:
        return ''


def func_st_date(x):
    """
    转换为日期格式，一般在pandas处理数据使用
    :param x: 日期时间格式，可能会有错误值
    :return:
    """
    try:
        return x.strftime('%Y-%m-%d')
    except:
        return ''


def func_st_time(x):
    """
    转换为时间格式，一般在pandas处理数据使用
    :param x: 日期时间格式，可能会有错误值
    :return:
    """
    try:
        return x.strftime('%H:%M:%S')
    except:
        return ''


def parse_html(html):
    lis = re.findall('>([^<]+)<', html)
    return [each.strip() for each in lis if each.strip()]


def get_outer_ip():
    """
    预计耗时0.87s
    :return:
    """
    url = 'http://ip.42.pl/raw'
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.text
    except:
        pass
    return ''


def get_outer_ip2():
    """
    预计耗时0.38s
    :return:
    """
    url = 'http://sspanel.net/ip.php'
    try:
        r = requests.get(url)
        if r.status_code == 200:
            ips = re.findall(r'((\d+\.){3}\d+)', r.text)
            if ips:
                return ips[0][0]
    except:
        pass
    return ''


def get_inner_ip():
    """
    预计耗时0.21s
    :return:
    """
    url = 'https://tools.getquicker.cn/api/Ip/MyIp'
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.text.strip()
    except:
        pass
    return ''


def get_lan_ip():
    """
    预计耗时0.00018s
    :return:
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    return s.getsockname()[0]


# 暂时使用本地数据读取
def get_user():
    if not IS_LOCAL:
        return ''
    path = os.path.join(os.environ['LOCALAPPDATA'], 'Quicker', 'data', 'static_data.ini')
    if not os.path.exists(path):
        return ''
    try:
        with open(path, 'r', encoding='utf-8') as f:
            st = f.read()
        return json.loads(st.replace('\ufeff', '')).get('user', '')
    except:
        return ''


# 用户信息需要考虑凭证过期问题
def update_user():
    ...


def date_add(date=None, days=0, st_format='str'):
    """
    取日期值，不带时间
    :param date: 初始日期，默认当天
    :param days: 增加天数
    :param st_format: 输出格式 str: 字符串格式, 其他: 日期格式
    :return:
    """
    if not date:
        date = datetime.today()
    if isinstance(date, str):
        date = datetime.strptime(date.split(' ')[0], '%Y-%m-%d')
    result_date = date + timedelta(days=days)
    date_st = result_date.strftime('%Y-%m-%d')
    if st_format == 'str':
        return date_st
    return datetime.strptime(date_st, '%Y-%m-%d')
