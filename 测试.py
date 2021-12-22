# -*- codeing = utf-8 -*-
# @Time : 2021/9/16 16:06
# @Author : 刘奇
# @File : 测试.py
# @Software : PyCharm
import json
import urllib, sys

# Define the parameters for the POST request and encode them in
# a URL-safe format.

# params = {
#     'js_code': "D:\Closure Compiler",
#     'compilation_level': 'WHITESPACE_ONLY',
#     'output_format': 'text',
#     'output_info': 'compiled_code'
# }
# params = json.dumps(params)
# # Always use the following value for the Content-type header.
# headers = { "Content-type": "application/x-www-form-urlencoded" }
# conn = urllib.request.Request(url='closure-compiler.appspot.com',data=params, headers=headers)
#
# response = urllib.request.urlopen(conn)
# data = response.read()
# print (data)
# conn.close()
k = []

a1 = {}
b1 = []
a1['s']='wang'
a1['w']=2
b1.append(a1)

a2 = {}
b2 = []
a2['s']='liu'
a2['w']=10
b2.append(a2)

a3 = {}
b3 = []
a3['s']='zhu'
a3['w']=-1
b3.append(a3)

a4 = {}
b4 = []
a4['s']='zheng'
a4['w']=-19
b4.append(a4)

k.extend(b1)
k.extend(b2)
k.extend(b3)
k.extend(b4)

print(k[0])

result = []
begin = k[0]
for i in range(1, len(k)):
    for j in range(0, len(k)-i):
        if k[j]['w']<k[j+1]['w']:
            k[j],k[j+1] = k[j+1],k[j]
print(k)
