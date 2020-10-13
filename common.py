#!/usr/bin/env python
# coding: utf-8
# @Time     : 2018/8/28 17:14
# @Author   : 你的名字啊！！！
# @FileName : LocustTestLibrary .py
# @Project  : YJiang

import os
import csv
import  codecs
import hashlib
import  logging
class Common:

    @staticmethod
    def abs_path(py_file, conf_dir=None):
        """
        返回文件的绝对路径
        :param py_file:文件对象__file__,或者是文件名  str
        :param conf_dir：默认直接去当前路径，如果此有值，在路径上加上此路径，str
        abs_path(__file__) 返回文件的目录路径
        abs_path(__file__，"data") 返回文件的目录路径/data
        """
        if conf_dir == None:conf_dir=""
        return os.path.normpath(
                   os.path.join(os.path.normpath(
                       os.path.dirname(os.path.realpath(py_file))), conf_dir))
                       
    @staticmethod
    def writerlog(level,log,logfile):
        log_filename = logfile
        log_format = '[%(asctime)s][%(levelname)s] %(message)s'
        logging.basicConfig(format = log_format,datefmt = '%Y-%m-%d %H:%M:%S %p',filename= log_filename,filemode='a',level=logging.INFO)
        logging.debug('---------------------------------------------------------------------')
        if level.upper() == 'ERROR':
            logging.error(log)
        elif level.upper() == 'INFO':
            logging.info(log)
        elif level.upper() == 'WARN':
            logging.warn(log)



    @staticmethod
    def incolorprint(contect,color=None,jibie =''):
        """

        :param contect: 打印内容
        :param color: 打印字体颜色，默认黑色
        :return:
        """
        if jibie =='error':
            if color != None:
                color = color.upper()
                if color == 'RED':
                    print( "{0}[1;31m{1}{2}[0m".format(chr(27),contect.encode('utf-8'),chr(27)))
                elif color == 'GREEN':
                    print ( "{0}[1;32m{1}{2}[0m".format(chr(27),contect.encode('utf-8'),chr(27)))

                elif color == 'YELLOW':
                    print ( "{0}[1;33m{1}{2}[0m".format(chr(27),contect.encode('utf-8'),chr(27)))
            else:
                print (contect)
        else:
            if color != None:
                color = color.upper()
                if color == 'RED':
                    print ( "{0}[31;2m{1}{2}[0m".format(chr(27),contect,chr(27)))
                elif color == 'GREEN':
                    print ( "{0}[32;2m{1}{2}[0m".format(chr(27),contect,chr(27)))

                elif color == 'YELLOW':
                    print ( "{0}[33;2m{1}{2}[0m".format(chr(27),contect,chr(27)))
            else:
                print (contect)

    @staticmethod
    def read_csv(file_path):
        content = []
        with codecs.open(file_path, mode='rb', errors='strict', buffering=1) as read_csv:
            read_contect = csv.DictReader(read_csv)
            for line in read_contect:
                content.append(line)
        return content


    @staticmethod
    def md5sum(context):
        md5 = hashlib.md5(context).hexdigest()
        return md5

    @staticmethod
    def filename(filepath):
        file_name = os.path.basename(filepath)
        return file_name

    @staticmethod
    def dirname(filepath):
        dir_name = os.path.dirname(filepath)
        return dir_name

    @staticmethod
    def GetPath(path_file,stag='.db'):


        AP=[os.path.join(x[0],y) for x in os.walk(path_file) for y in x[2] if os.path.splitext(y)[1] == stag]
        return AP



