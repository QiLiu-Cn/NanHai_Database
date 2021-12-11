# -*- coding:utf-8 -*-
from django.shortcuts import render
from Model.neo_models import Neo4j

neo_con = Neo4j()   #预加载neo4j
neo_con.connectDB()
db = neo_con

def question_answering(request):  # index页面需要一开始就加载的内容写在这里
	context = {'ctx':''}
	return render(request, 'question_answering.html', context)