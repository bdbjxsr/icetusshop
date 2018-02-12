# coding=utf-8
import pymysql
pymysql.install_as_MySQLdb()
#在这里先注册一下register，不然后面自定义标签可能不生效
from django import template
register = template.Library()