#!/usr/bin/env python
# coding: utf-8
# @Time     : 2018/8/28 17:14
# @Author   : 你的名字啊！！！
# @FileName : LocustTestLibrary .py
# @Project  : YJiang

import datetime
import inspect
import sqlite3

import maya_api.service.common as common

from collections import defaultdict

class Search:
    def __init__(self):

        self._sql_connect = common.Common.abs_path(__file__, 'Happy.db')

    def user_Id(self):
        """
        获取人员主题结构并排序,目前现场主题库表结构暂未确定，目前只统计涉及输出的字段。
        :return:
        """
        connect = sqlite3.connect(self._sql_connect)
        cursor = connect.cursor()

        search_sql = "SELECT user_Id from basic_user_information "

        select = cursor.execute(search_sql)
        result = select.fetchall()
        all_user_Id = []
        for line in result:
            all_user_Id.append(line[0])
        cursor.close()
        connect.close()
        return all_user_Id


class Create:
    """
    初始化建表
    """

    def __init__(self):
        self._sql_connect = common.Common.abs_path(__file__, 'Happy.db')

    def basic_user_information(self):
        """
        基本信息表
        :return:
        """
        connect = sqlite3.connect(self._sql_connect)
        cursor = connect.cursor()
        # 表结构：用户iD  用户名、 游戏场次、总计支出、总计收入、净收入、活跃状态、用户级别、注册时间

        create_sql = 'create table IF NOT EXISTS basic_user_information (user_Id INT PRIMARY KEY , ' \
                     'user_name CHAR(20) NOT NULL , ' \
                     'total_sessions INT NOT NULL, ' \
                     'total_expenses INT NOT NULL ,' \
                     'total_revenue INT NOT NULL, ' \
                     'net_income INT NOT NULL,' \
                     'active_status CHAR(50) NOT NULL, ' \
                     'user_leve INT NOT NULL,' \
                     'registration_time CHAR(50) NOT NULL)'

        cursor.execute(create_sql)
        connect.commit()
        cursor.close()
        connect.close()

    def run_all(self):
        """

        :return:
        """
        for func in inspect.getmembers(self, predicate=inspect.ismethod):
            if func[0] not in ['run_all', '__init__']: func[1]()


class Insert:
    """
    1.字典表：初始化字典数据。
    2.结果表：数据插入
    """

    def __init__(self):
        self._sql_connect = common.Common.abs_path(__file__, 'Happy.db')

    def basic_user_information(self, result):
        connect = sqlite3.connect(self._sql_connect)
        cursor = connect.cursor()
        insert_sql = "insert into basic_user_information (user_Id," \
                             "user_name," \
                             "total_sessions ," \
                             "total_expenses," \
                             "total_revenue," \
                             "net_income," \
                             "active_status," \
                             "user_leve ," \
                             "registration_time) " \
                     "VALUES (:user_Id," \
                             ":user_name," \
                             ":total_sessions ," \
                             ":total_expenses, " \
                             ":total_revenue, " \
                             ":net_income," \
                             ":active_status, " \
                             ":user_leve ," \
                             ":registration_time)"  # REPLACE

        try:
            cursor.execute(insert_sql,
                           result)
        except :
            log = u'ERROR INSERT basic_user_information {0} '.format(result['user_Id'])
            common.Common.incolorprint(log, 'red')

        else:

            log = 'INFO INSERT basic_user_information SUCCESS {0}'.format(result['user_Id'])
            common.Common.incolorprint(log, 'GREEN')
        connect.commit()
        connect.close()




class Update:
    """
    1.字典表：初始化字典数据。
    2.结果表：数据插入
    """

    def __init__(self):
        self._sql_connect = common.Common.abs_path(__file__, 'Happy.db')


    def settlement_signal_gun_activity(self,sessions):
        connect = sqlite3.connect(self._sql_connect)
        cursor = connect.cursor()

        update_sql = "UPDATE signal_gun_activity SET settlement_status= '已结算' WHERE sessions= '{0}';".format(sessions)

        try:
            cursor.execute(update_sql)
        except :
            log = u'ERROR UPDATE signal_gun_activity'
            common.Common.incolorprint(log, 'red')

        else:
            pass
            log = 'INFO UPDATE signal_gun_activity SUCCESS '
            common.Common.incolorprint(log, 'GREEN')
        connect.commit()
        connect.close()


class Delete:
    def __init__(self):
        self._sql_connect = common.Common.abs_path(__file__, 'Locust.db')

    def delete_table(self, tablename):
        connect = sqlite3.connect(self._sql_connect)
        cursor = connect.cursor()

        create_sql = 'delete from {0}'.format(tablename)
        cursor.execute(create_sql)
        log = 'INFO DELETE {0} SUCCESS '.format(tablename)
        common.Common.incolorprint(log, 'GREEN')
        cursor.close()
        connect.commit()
        connect.close()


class MainInit:
    def __init__(self, init=True):
        if init:
            # 初始化建表
            Create().run_all()


if __name__ == "__main__":
    MainInit()

