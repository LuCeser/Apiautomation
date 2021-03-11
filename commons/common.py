#!/usr/bin/env python
# encoding: utf-8
"""
#-------------------------------------------------------------------
#                   CONFIDENTIAL --- WellCloud                           
#-------------------------------------------------------------------
#                                                                   
#                   @Project Name : Apiautomation                 
#                                                                   
#                   @File Name    : common.py.py                      
#                                                                   
#                   @Programmer   : zhanglu                          
#                                                                     
#                   @Start Date   : 2021/3/11 10:49                 
#                                                                   
#                   @Last Update  : 2021/3/11 10:49                 
#                   
#                   @Description  : 提供通用函数
#                                                                   
#-------------------------------------------------------------------
# Classes:                                                          
#                                                                   
#-------------------------------------------------------------------
"""


def login(username, password):
    """
    登陆方法，可以被调用
    :param username: 用户名
    :param password: 密码
    :return:
    """
    print("login: username %s, password %s" % (username, password))
