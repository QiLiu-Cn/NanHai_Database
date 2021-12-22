# -*- coding: utf-8 -*-
from django.shortcuts import render
from Model.neo_models import Neo4j
import os

neo_con = Neo4j()   #预加载neo4j
neo_con.connectDB()
print('neo4j connected!')

import json
relationCountDict = {}
filePath = os.path.abspath(os.path.join(os.getcwd(),"."))
with open(filePath+"/toolkit/relationStaticResult.txt","r",encoding='utf8') as fr:
	for line in fr:
		relationNameCount = line.split(",")
		relationName = relationNameCount[0][2:-1]
		relationCount = relationNameCount[1][1:-2]
		relationCountDict[relationName] = int(relationCount)
def sortDict(relationDict):
	for i in range( len(relationDict) ):
		relationName = relationDict[i]['rel']['type']
		relationCount = relationCountDict.get(relationName)
		if(relationCount is None ):
			relationCount = 0
		relationDict[i]['relationCount'] = relationCount

	relationDict = sorted(relationDict,key = lambda item:item['relationCount'],reverse = True)

	return relationDict

def sort(relationDict):
	for i in range( len(relationDict) ):
		relationName = relationDict[i]['n1']['name']
		relationCount = relationCountDict.get(relationName)
		if(relationCount is None ):
			relationCount = 0
		relationDict[i]['relationCount'] = relationCount

	relationDict = sorted(relationDict,key = lambda item:item['relationCount'],reverse = True)

	return relationDict

def search_entity(request):
	ctx = {}
	#根据传入的实体名称搜索出关系
	if(request.GET):
		entity = request.GET['user_text']
		#连接数据库
		db = neo_con
		entityRelation = db.getEntityRelationbyEntity(entity)
		if len(entityRelation) == 0:
			#若数据库中无法找到该实体，则返回数据库中无该实体
			ctx= {'title' : '<h1>数据库中暂未添加该实体</h1>'}
			return render(request,'entity.html',{'ctx':json.dumps(ctx,ensure_ascii=False)})
		else:
			#返回查询结果
			#将查询结果按照"关系出现次数"的统计结果进行排序
			entityRelation = sortDict(entityRelation)

			return render(request,'entity.html',{'entityRelation':json.dumps(entityRelation,ensure_ascii=False)})

	return render(request,"entity.html",{'ctx':ctx})

def search_in(request):
	ctx = {}
	if (request.GET):
		db = neo_con
		entity1 = ''
		relation = request.GET['relation_name_text']
		entity2 = request.GET['entity2_text']
		relation = relation.lower()
		searchResult = {}

		# 若只输入entity2则,则输出与entity2有直接关系的实体和关系
		if (len(entity2) != 0 and len(relation) == 0 and len(entity1) == 0):
			searchResult = db.findRelationByEntity2(entity2)
			searchResult = sortDict(searchResult)
			if (len(searchResult) > 0):
				return render(request, 'relation.html', {'searchResult': json.dumps(searchResult, ensure_ascii=False)})

		# 若输入entity2和relation，则输出与entity2具有relation关系的其他实体
		if (len(entity2) != 0 and len(relation) != 0 and len(entity1) == 0):
			searchResult = db.findOtherEntities2(entity2, relation)
			searchResult = sortDict(searchResult)
			if (len(searchResult) > 0):
				return render(request, 'relation.html', {'searchResult': json.dumps(searchResult, ensure_ascii=False)})

		# 全为空
		if (len(entity1) != 0 and len(relation) != 0 and len(entity2) != 0):
			pass
		ctx = {'title': '<h1>暂未找到相应的匹配</h1>'}
		return render(request, 'relation.html', {'ctx': ctx})

	return render(request, 'relation.html', {'ctx': ctx})

def search_relation(request):
	ctx = {}
	if(request.GET):
		db = neo_con
		entity1 = request.GET['entity1_text']
		relation = request.GET['relation_name_text']
		entity2 = request.GET['entity2_text']
		relation = relation.lower()
		searchResult = {}
		#若只输入entity1,则输出与entity1有直接关系的实体和关系
		if(len(entity1) != 0 and len(relation) == 0 and len(entity2) == 0):
			searchResult = db.findRelationByEntity(entity1)
			searchResult = sortDict(searchResult)
			if(len(searchResult)>0):
				return render(request,'search_road.html',{'searchResult':json.dumps(searchResult,ensure_ascii=False)})

		#若只输入entity2则,则输出与entity2有直接关系的实体和关系
		if(len(entity2) != 0 and len(relation) == 0 and len(entity1) == 0):
			searchResult = db.findRelationByEntity2(entity2)
			searchResult = sortDict(searchResult)
			if(len(searchResult)>0):
				return render(request,'search_road.html',{'searchResult':json.dumps(searchResult,ensure_ascii=False)})
		#若输入entity1和relation，则输出与entity1具有relation关系的其他实体
		if(len(entity1)!=0 and len(relation)!=0 and len(entity2) == 0):
			searchResult = db.findOtherEntities(entity1,relation)
			searchResult = sortDict(searchResult)
			if(len(searchResult)>0):
				return render(request,'search_road.html',{'searchResult':json.dumps(searchResult,ensure_ascii=False)})
		#若输入entity2和relation，则输出与entity2具有relation关系的其他实体
		if(len(entity2)!=0 and len(relation)!=0 and len(entity1) == 0):
			searchResult = db.findOtherEntities2(entity2,relation)
			searchResult = sortDict(searchResult)
			if(len(searchResult)>0):
				return render(request,'search_road.html',{'searchResult':json.dumps(searchResult,ensure_ascii=False)})
		#若输入entity1和entity2,则输出entity1和entity2之间的最短路径
		if(len(entity1) !=0 and len(relation) == 0 and len(entity2)!=0):
			searchResult = db.findRelationByEntities(entity1,entity2)
			if(len(searchResult)>0):
				# print(searchResult)
				searchResult = sortDict(searchResult)
				return render(request,'search_road.html',{'searchResult':json.dumps(searchResult,ensure_ascii=False)})
		#若输入entity1,entity2和relation,则输出entity1、entity2是否具有相应的关系
		if(len(entity1)!=0 and len(entity2)!=0 and len(relation)!=0):
			searchResult = db.findEntityRelation(entity1,relation,entity2)
			if(len(searchResult)>0):
				return render(request,'search_road.html',{'searchResult':json.dumps(searchResult,ensure_ascii=False)})
		#全为空
		if(len(entity1)!=0 and len(relation)!=0 and len(entity2)!=0 ):
			pass
		ctx= {'title' : '<h1>暂未找到相应的匹配</h1>'}
		return render(request,'search_road.html',{'ctx':ctx})

	return render(request,'search_road.html',{'ctx':ctx})


def search_proof(request):
	ctx = {}
	if (request.GET):
		db = neo_con
		entity1 = request.GET['entity1_text']

		searchResult = {}
		# 若只输入entity1,则输出与entity1有直接关系的实体和关系
		if (len(entity1) != 0):
			searchResult = db.findProof(entity1)
			# searchResult = sortDict(searchResult)
			if(len(searchResult)>0):
				return  render(request,'zhengminglidaxiao.html',{'searchResult':json.dumps(searchResult,ensure_ascii=False)})

		else:
			pass

		ctx = {'title': '<h1>暂未找到相应的匹配</h1>'}
		return render(request, 'zhengminglidaxiao.html', {'ctx': ctx})

	return render(request, 'zhengminglidaxiao.html', {'ctx': ctx})

def proof(request):
	ctx = {}
	if (request.GET):
		db = neo_con
		entity1 = request.GET['entity1_text']

		searchResult = []
		# 若只输入entity1,则输出与entity1有直接关系的实体和关系
		if (len(entity1) != 0):
			searchResult1 = db.findRelationByEntity2(entity1)
			searchResult1 = sortDict(searchResult1)
			if(len(searchResult1)>0):
				for i in range(len(searchResult1)):
					name = searchResult1[i]['n1']['name']
					searchResult2=db.findProof(name)

					if len(searchResult2) != 0:
						searchResult.extend(searchResult2)
			for i in range(1, len(searchResult)):
				for j in range(0, len(searchResult) - i):
					if searchResult[j]['score'] < searchResult[j + 1]['score']:
						searchResult[j], searchResult[j + 1] = searchResult[j + 1], searchResult[j]
			# searchResult = sort(searchResult)

			return render(request,'type_display.html',{'searchResult':json.dumps(searchResult,ensure_ascii=False)})
		else:
			pass

		ctx = {'title': '<h1>暂未找到相应的匹配</h1>'}
		return render(request, 'type_display.html', {'ctx': ctx})

	return render(request, 'type_display.html', {'ctx': ctx})

# def search_attribute(request):
