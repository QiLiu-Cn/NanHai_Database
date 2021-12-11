# -*- coding: utf-8 -*-
import thulac
import csv
import sys
import os
sys.path.append("..")

from Model.neo_models import Neo4j 
from Model.mongo_model import Mongo
from toolkit.tree_API import TREE

filePath = os.getcwd()

# 读取农业层次树
tree = TREE()
tree.read_edge(filePath+'/toolkit/micropedia_tree.txt')
tree.read_leaf(filePath+'/toolkit/leaf_list.txt')
		
print('level tree load over~~~')
