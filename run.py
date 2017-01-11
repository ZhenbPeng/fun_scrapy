# -*- coding: utf-8 -*-
# AUTHOR: ZhenbPeng
# DATE: 1/11/2017
# TIME: 6:42 PM
import gevent
import logging.config
from gevent import monkey; monkey.patch_socket()
from scrapy.cmdline import execute



if __name__ == '__main__':
    logging.config.fileConfig("log.conf")
    e = gevent.spawn(execute)
    gevent.joinall([e])