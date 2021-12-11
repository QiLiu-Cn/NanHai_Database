# -*- codeing = utf-8 -*-
# @Time : 2021/8/30 14:41
# @Author : 刘奇
# @File : neo4j.py
# @Software : PyCharm

from neo4j import GraphDatabase

driver = GraphDatabase.driver('cloud@210.28.132.120',auth=('NJU-stly-server','passwOrd'))

