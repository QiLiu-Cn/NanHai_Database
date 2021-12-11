from py2neo import Graph, Node, Relationship, cypher, Path
import neo4j
class Neo4j():
	graph = None
	def __init__(self):
		print("create neo4j class ...")

	def connectDB(self):
		self.graph = Graph("bolt://localhost:7687", username="neo4j", password="passw0rd")

	def matchItembyTitle(self,value):

		sql = "MATCH (n:Item { title: '" + str(value) + "' }) return n;"
		answer = self.graph.run(sql).data()
		return answer

	# 根据title值返回互动百科item
	def matchHudongItembyTitle(self,value):
		sql = "MATCH (n:HudongItem { title: '" + str(value) + "' }) return n;"
		try:
			answer = self.graph.run(sql).data()
		except:
			print(sql)
		return answer

	# 根据entity的名称返回关系
	def getEntityRelationbyEntity(self,value):
		answer = self.graph.run("MATCH (entity1) - [rel] -> (entity2)  WHERE entity1.name = \"" +str(value)+"\" RETURN entity1,rel,entity2").data()
		return answer

	#查找entity1及其对应的关系（与getEntityRelationbyEntity的差别就是返回值不一样）
	def findRelationByEntity(self,entity1):
		answer = self.graph.run("MATCH (n1 {name:\""+str(entity1)+"\"})- [rel] -> (n2) RETURN n1,rel,n2" ).data()
		# if(answer is None):
		# 	answer = self.graph.run("MATCH (n1:NewNode {title:\""+entity1+"\"})- [rel] -> (n2) RETURN n1,rel,n2" ).data()
		return answer

	#查找entity2及其对应的关系
	def findRelationByEntity2(self,entity1):
		answer = self.graph.run("MATCH (n1)- [rel] -> (n2 {name:\""+str(entity1)+"\"}) RETURN n1,rel,n2" ).data()
		# if(answer is None):
		# 	answer = self.graph.run("MATCH (n1)- [rel] -> (n2:NewNode {title:\""+entity1+"\"}) RETURN n1,rel,n2" ).data()
		return answer

	#根据entity1和关系查找enitty2
	def findOtherEntities(self,entity,relation):
		answer = self.graph.run("MATCH (n1 {name:\"" + str(entity) + "\"})- [rel {type:\""+str(relation)+"\"}] -> (n2) RETURN n1,rel,n2" ).data()
		#if(answer is None):
		#	answer = self.graph.run("MATCH (n1:NewNode {title:\"" + entity + "\"})- [rel:RELATION {type:\""+relation+"\"}] -> (n2) RETURN n1,rel,n2" ).data()

		return answer

	#根据entity2和关系查找enitty1
	def findOtherEntities2(self,entity,relation):
		answer = self.graph.run("MATCH (n1)- [rel {type:\""+str(relation)+"\"}] -> (n2 {name:\"" + str(entity) + "\"}) RETURN n1,rel,n2" ).data()
		#if(answer is None):
		#	answer = self.graph.run("MATCH (n1)- [rel:RELATION {type:\""+relation+"\"}] -> (n2:NewNode {title:\"" + entity + "\"}) RETURN n1,rel,n2" ).data()

		return answer

	#根据两个实体查询它们之间的最短路径
	def findRelationByEntities(self,entity1,entity2):
		answer = self.graph.run("MATCH (p1:地点{name:\"" + str(entity1) + "\"}),(p2:主体{name:\""+str(entity2)+"\"}),p=shortestpath((p1)-[rel:rel*]-(p2)) RETURN rel").evaluate()
		#answer = self.graph.run("MATCH (p1:HudongItem {title:\"" + entity1 + "\"})-[rel:RELATION]-(p2:HudongItem{title:\""+entity2+"\"}) RETURN p1,p2").data()
		
		if(answer is None):	
			answer = self.graph.run("MATCH (p1:地点{name:\"" + str(entity1) + "\"}),(p2:证据主题{name:\""+str(entity2)+"\"}),p=shortestpath((p1)-[rel:rel*]-(p2)) RETURN p").evaluate()
		if (answer is None):
			answer = self.graph.run("MATCH (p1:地点{name:\"" + str(entity1) + "\"}),(p2:地点{name:\"" + str(
				entity2) + "\"}),p=shortestpath((p1)-[rel:rel*]-(p2)) RETURN p").evaluate()
		if (answer is None):
			answer = self.graph.run("MATCH (p1:证据源形式{name:\"" + str(entity1) + "\"}),(p2:证据源形式{name:\"" + str(
				entity2) + "\"}),p=shortestpath((p1)-[rel:rel*]-(p2)) RETURN p").evaluate()
		if (answer is None):
			answer = self.graph.run("MATCH (p1:证据主题{name:\"" + str(entity1) + "\"}),(p2:证据主题{name:\"" + str(
				entity2) + "\"}),p=shortestpath((p1)-[rel:rel*]-(p2)) RETURN p").evaluate()
		if (answer is None):
			answer = self.graph.run("MATCH (p1:主体{name:\"" + str(entity1) + "\"}),(p2:主体{name:\"" + str(
				entity2) + "\"}),p=shortestpath((p1)-[rel:rel*]-(p2)) RETURN p").evaluate()
		if (answer is None):
			answer = self.graph.run("MATCH (p1:地点{name:\"" + str(entity1) + "\"}),(p2:证据源形式{name:\"" + str(
				entity2) + "\"}),p=shortestpath((p1)-[rel:rel*]-(p2)) RETURN p").evaluate()
		if (answer is None):
			answer = self.graph.run("MATCH (p1:地点{name:\"" + str(entity1) + "\"}),(p2:主体{name:\"" + str(
				entity2) + "\"}),p=shortestpath((p1)-[rel:rel*]-(p2)) RETURN p").evaluate()
		relationDict = []
		if(answer is not None):
			for x in answer:
				tmp = {}
				start_node = x.start_node
				end_node = x.end_node
				tmp['n1'] = start_node
				tmp['n2'] = end_node
				tmp['rel'] = x
				relationDict.append(tmp)		
		return relationDict

	#查询数据库中是否有对应的实体-关系匹配
	def findEntityRelation(self,entity1,relation,entity2):
		answer = self.graph.run("MATCH (n1:HudongItem {title:\"" + str(entity1) + "\"})- [rel:RELATION {type:\""+str(relation)+"\"}] -> (n2:HudongItem{title:\""+entity2+"\"}) RETURN n1,rel,n2" ).data()
		if(answer is None):
			answer = self.graph.run("MATCH (n1:HudongItem {title:\"" + str(entity1) + "\"})- [rel:RELATION {type:\""+str(relation)+"\"}] -> (n2:NewNode{title:\""+entity2+"\"}) RETURN n1,rel,n2" ).data()
		if(answer is None):
			answer = self.graph.run("MATCH (n1:NewNode {title:\"" + str(entity1) + "\"})- [rel:RELATION {type:\""+str(relation)+"\"}] -> (n2:HudongItem{title:\""+entity2+"\"}) RETURN n1,rel,n2" ).data()
		if(answer is None):
			answer = self.graph.run("MATCH (n1:NewNode {title:\"" + str(entity1) + "\"})- [rel:RELATION {type:\""+str(relation)+"\"}] -> (n2:NewNode{title:\""+entity2+"\"}) RETURN n1,rel,n2" ).data()

		return answer

	#数据库中的属性共现关联
	def findAttributeDispaly(self,entity1,rel,entity2):
		if entity1 is not None:
			answer = self.graph.run("MATCH (n1 {name:\"" + str(entity1) + "\"})- [rel] -> (n2) RETURN n1,rel,n2").data()
		# if (answer is None):
		# 	answer = self.graph.run("MATCH (n1) - [rel {type:\"" + str(entity1) + "\"}] -> (n2) RETURN n1,ref,n2").data()
		# if (answer is None):
		# 	answer = self.graph.run("MATCH (n1)- [rel] -> (n2 {name:\"" + str(entity1) + "\"}) RETURN n1,ref,n2").data()

		return answer


	# 数据库中的证明力大小关联
	def findProof(self,entity1):
		s1 = 0.5
		s2 = 0.7
		relationDict = []
		relationDict1 = []
		relationDict2 = []
		answer1 = self.graph.run("MATCH (n1:证据编号 {name:\""+str(entity1)+"\"})- [rel:rel*] -> (n2:证据源) RETURN n1,rel,n2").data()
		answer2 = self.graph.run("MATCH (n3:证据编号 {name:\"" + str(entity1) + "\"})- [rel:rel*] -> (n4:证据主题) RETURN n3,rel,n4").data()

		if (answer1 is not None ):
			if (answer2 is not None):
			# for i in range(0,len(answer1)):
			# 	tmp = {}
			# 	start_node1 = answer1[i].start_node
			# 	end_node1 = answer1[i].end_node
			# 	end_node2 = answer2[i].end_node
			# 	tmp['n1'] = start_node1
			# 	tmp['n2'] = end_node1
			# 	tmp['s1'] = s1
			# 	tmp['n3'] = end_node2
			# 	tmp['s2'] = s2
			# 	tmp['s'] = s1*s2
			# 	relationDict.append(tmp)
			# for i in answer1:
			# 	tmp = {}
			# 	start_node1 = i.start_node
			# 	end_node1 = i.end_node
			# 	tmp['n1'] = start_node1
			# 	tmp['n2'] = end_node1
			# 	tmp['s1'] = str(s1)
			# 	relationDict1.append(tmp)
			# for j in answer2:
			# 	tmp = {}
			# 	end_node2 = j.end_node
			# 	tmp['n3'] = end_node2
			# 	tmp['s2'] = str(s2)
			# 	tmp['s'] = str(s1 * s2)
			# 	relationDict2.append(tmp)
				for i in range(0,len(answer2)):
					tmp = {}
					tmp['n1'] = answer1[i]['n1']
					tmp['n2'] = answer1[i]['n2']
					tmp['s1'] = str(s1)
					tmp['n3'] = answer2[i]['n4']
					tmp['s2'] = str(s2)
					tmp['s'] = str(s1*s2)
					relationDict.append(tmp)
		return relationDict



	# def findattribute(self,entiyu1):

