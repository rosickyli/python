# -*- coding:utf-8 -*-
import urllib
import urllib.request
import re
import cx_Oracle
import os
import datetime
import bs4

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
lis=[]
i=0
citys=[
101020100,
101180101,
101191101,
101210101,
101240101,
101010100,
101190101,
101030100,
101190801,
101190401,
101210401,
101110101,
101250101,
101040100,
101270101,
101120101,
101120201,
101190501,
101280601,
101281601,
101280101,
101200101,
101250401]
names=['上海市',
 '郑州市',
 '常州市',
 '杭州市',
 '南昌市',
 '北京市',
 '南京市',
 '天津市',
 '徐州市',
 '苏州市',
 '宁波市',
 '西安市',
 '长沙市',
 '重庆市',
 '成都市',
 '济南市',
 '青岛市',
 '南通市',
 '深圳市',
 '东莞市',
 '广州市',
 '武汉市',
 '衡阳市']
while (i<len(citys)):
    code=citys[i]
    # print(names[i])
    lis.append(names[i])
    url = 'http://www.weather.com.cn/weather/%d.shtml' % code
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = {'User-Agent': user_agent}
    try:
        response = urllib.request.urlopen(url)
        content = response.read().decode('utf-8')
        pat_weather = re.compile('<input type="hidden" id="hidden_title" value="(.*?)" />')
        weather = pat_weather.findall(content)
        #print(weather[0])
        td = datetime.datetime.now().strftime('%Y-%m-%d')
        z=td+' '+weather[0]
        #print(z)
        lis.append(z)
    except urllib.request.URLError as e:
        if hasattr(e, "code"):
            print
            e.code
        if hasattr(e, "reason"):
            print
            e.reason
    i=i+1


#print (lis)
dic={}
for j in range(0,len(lis),2):
    dic[lis[j]]=lis[j+1]
#print (dic)
conn = cx_Oracle.connect('usrname/pwd@ip:1521/dbname')
c = conn.cursor()
for k,v in dic.items():
    sql = "insert into ldreport.dw_weather(city,weather) values(\'%s\',\'%s\')" % (k, v)
    #print(sql)
    try:
        c.execute(sql)
        conn.commit()
    except:
        conn.rollback()
c.close()
conn.close()
