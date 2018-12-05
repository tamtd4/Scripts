#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 03/01/2017
Author: Long Chen
Description: A script to get MongoDB metrics
Requires: MongoClient in python
"""
import json
from calendar import timegm
from time import gmtime

from pymongo import MongoClient, errors
from sys import exit
import urllib
from sys import argv
#import urllib.parse
class MongoDB(object):
    """main script class"""
    # pylint: disable=too-many-instance-attributes
    def __init__(self,**kwargs):
        self.mongo_host = kwargs['mongo_host']
        self.mongo_port = kwargs['mongo_port']
        self.mongo_db = ["admin" ]
        self.mongo_user = kwargs['mongo_user']
        # 转化密码中的特殊字符，如@
        self.mongo_password = urllib.parse.quote(kwargs['mongo_pwd'])
        self.__conn = None
        self.__dbnames = None
        self.__metrics = []
    
        #print(kwargs)

    def connect(self):
        """Connect to MongoDB"""
        if self.__conn is None:
            if self.mongo_user is None:
                try:
                    self.__conn = MongoClient('mongodb://%s:%s' %
                                              (self.mongo_host,
                                               self.mongo_port))
                except errors.PyMongoError as py_mongo_error:
                    print('Error in MongoDB connection: %s' %
                          str(py_mongo_error))
            else:
                try:
                    self.__conn = MongoClient('mongodb://%s:%s@%s:%s' %
                                              (self.mongo_user,
                                               self.mongo_password,
                                               self.mongo_host,
                                               self.mongo_port))
                except errors.PyMongoError as py_mongo_error:
                    print('Error in MongoDB connection: %s' %
                          str(py_mongo_error))

    def add_metrics(self, k, v):
        """add each metric to the metrics list"""
        dict_metrics = {}
        dict_metrics['key'] = k
        dict_metrics['value'] = v
        self.__metrics.append(dict_metrics)

    def print_metrics(self):
        """print out all metrics"""
        metrics = self.__metrics
        for metric in metrics:
            zabbix_item_key = str(metric['key'])
            zabbix_item_value = metric['value']
            print(json.dumps({"data": zabbix_item_value}, indent=4))
            
    def get_db_names(self):
        """get a list of DB names"""
        if self.__conn is None:
            self.connect()
        db_handler = self.__conn[self.mongo_db[0]]

        master = db_handler.command('isMaster')['ismaster']
        dict_metrics = {}
        dict_metrics['key'] = 'ismaster'
        if master:
            dict_metrics['value'] = 1
            db_names = self.__conn.database_names()
            self.__dbnames = db_names
        else:
            dict_metrics['value'] = 0
        #self.__metrics.append(dict_metrics)

    def get_mongo_db_lld(self):
        """print DB list in json format, to be used for
        mongo db discovery in zabbix"""
        if self.__dbnames is None:
            db_names = self.get_db_names()

        else:
            db_names = self.__dbnames
        dict_metrics = {}
        db_list = []
        dict_metrics['key'] = 'discovery'
        dict_metrics['value'] = {"data": db_list}
        if db_names is not None:
            for db_name in db_names:
                dict_lld_metric = {}
                dict_lld_metric['{#MONGODBNAME}'] = db_name
                db_list.append(dict_lld_metric)
            dict_metrics['value'] =  db_list
        self.__metrics.insert(0, dict_metrics)


    def close(self):
        """close connection to mongo"""
        if self.__conn is not None:
            self.__conn.close()
        
if __name__ == '__main__':
#    print 'arg:{0}'.format(argv)
    mongodb = MongoDB(mongo_host=argv[1],mongo_port=argv[2],mongo_user=argv[3],mongo_pwd=argv[4])
    mongodb.get_db_names()
    mongodb.get_mongo_db_lld()
    mongodb.print_metrics()
    mongodb.close()

