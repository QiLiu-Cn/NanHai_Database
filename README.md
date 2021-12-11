**0.安装基本环境：**

确保安装好python3和Neo4j（任意版本）
 
安装一系列pip依赖： cd至项目根目录，运行 sudo pip3 install -r requirement.txt

**1.导入数据：**

将neo4j文件夹下的各csv文件导入neo4j：开启neo4j，进入neo4j控制台。名字中无下划线符号的是节点数据，有下划线的是关系数据，下划线前后分别对应两种类型的节点，先导入节点数据，再导入关系数据。
例：将count.csv放入neo4j安装目录下的/import目录。在控制台依次输入：

```
// 将hudong_pedia.csv 导入
LOAD CSV WITH HEADERS  FROM "file:///count.csv" AS line  
CREATE (p:证据编号{name:line.num,content:line.con})  
//证据编号是节点类型名，name和content是定义的节点属性，分别对应每一行数据中的“num”和“con”，“num”和“con”是csv文件中的列索引名。
```
```
// 创建索引
CREATE CONSTRAINT ON (c:证据编号)
ASSERT c.name IS UNIQUE
```
以上两步的意思是，将count.csv导入neo4j作为结点，然后对name属性添加UNIQUE（唯一约束/索引）

*（如果导入的时候出现neo4j jvm内存溢出，可以在导入前，先把neo4j下的conf/neo4j.conf中的dbms.memory.heap.initial_size 和dbms.memory.heap.max_size调大点。导入完成后再把值改回去）*

//导入节点之间的关系，示例
LOAD CSV  WITH HEADERS FROM "file:///cou_loc.csv" AS line
MATCH (from:证据编号{name:line.cout}) , (to:地点{name:line.loc})
CREATE (from)-[:hasrelation{ type: line.type }]->(to)
//证据编号和地点分别是两种类型的节点，name是两种类型节点的主属性，cout、loc和type是列索引名


**3.修改Neo4j用户**

进入demo/Model/neo_models.py,修改第9行的neo4j账号密码，改成待链接数据库的用户名和密码

**4.连接MySQL导入证据文本**

demo/demo/settings.py下，改变DATABASES变量约78行左右，改为MySQL数据库的用户名和密码
将文件夹目录下mysql_data.csv导入建好的表

**5.启动服务**

进入demo目录，然后运行脚本：

```
sudo sh django_server_start.sh
```

这样就成功的启动了django。进入8000端口主页面，就是网站主页。
表示模型、关联模型、属性贡献

#叙事脉络关联、逻辑论证关联、证明力大小关联、属性贡献关联