# -*- codeing = utf-8 -*-
# @Time : 2021/9/16 16:06
# @Author : 刘奇
# @File : 测试.py
# @Software : PyCharm
import json
import urllib, sys

# Define the parameters for the POST request and encode them in
# a URL-safe format.

params = {
    'js_code': "D:\Closure Compiler",
    'compilation_level': 'WHITESPACE_ONLY',
    'output_format': 'text',
    'output_info': 'compiled_code'
}
params = json.dumps(params)
# Always use the following value for the Content-type header.
headers = { "Content-type": "application/x-www-form-urlencoded" }
conn = urllib.request.Request(url='closure-compiler.appspot.com',data=params, headers=headers)

response = urllib.request.urlopen(conn)
data = response.read()
print (data)
conn.close()
