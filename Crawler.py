# -*- coding: UTF-8 -*-
#!pip install selenium
#!pip install webdriver_manager

import os
import time
from urllib import request

# import
try:
    from bs4 import BeautifulSoup
    from selenium import webdriver
    from webdriver_manager.chrome import ChromeDriverManager
    import pymysql
except:
    os.system("pip3 install beautifulsoup4")
    os.system("pip3 install selenium")
    os.system("pip3 install webdriver-manager")
    os.system("pip3 install PyMySQL")
    from bs4 import BeautifulSoup
    from selenium import webdriver
    from webdriver_manager.chrome import ChromeDriverManager
    import pymysql

is_use_engine = False

"""
map规范:
- 空格用于防止key重名
- 逗号用于分开元素名和class
"""
class Crawler:
    def __init__(self,url):
        self.url = url
        self.insertMap = {}
        

    def search(self,sitelist,catch_map,sleepTime=1,fun=None):
        for i in sitelist:
            if self.url[0:4] == 'http':
                if is_use_engine:
                    # 启动浏览器
                    browserEngine = webdriver.Chrome(ChromeDriverManager().install())
                    browserEngine.get(self.url.format(i))
                    # 等待
                    browserEngine.implicitly_wait(60)
                    time.sleep(sleepTime)
                    page_source = browserEngine.page_source
                    # 关闭浏览器
                    browserEngine.quit()
                else:
                    headers = {'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Mobile Safari/537.36'}
                    # 创建请求
                    req = request.Request(url=self.url.format(i), headers=headers)
                    # time.sleep(0.5)
                    with request.urlopen(req) as response:
                        # 读取response里的内容，并转码
                        page_source = response.read().decode('utf-8') # 默认即为 utf-8

            else:
                page_source = open(self.url).read()
            # 进行搜索
            self.browser = BeautifulSoup(page_source, 'html.parser')
            self.__find(catch_map,[self.browser])
            # 检测有无方法并运行
            if fun != None:
                try:
                    fun(i,self.insertMap)
                except Exception:
                    pass
                self.insertMap = {}
        return self.insertMap
    def __find(self,cmap,browserList:list):
        if isinstance(cmap,dict):
            index = 0
            if len(browserList)<len(cmap):
                print('点数:'+ str(len(browserList))+ '少于键数:' + str(len(cmap)))
                return
            for i in cmap.keys():
                # 由于key不能重复,启用丢弃空格后的方案
                searchStrs = i.split(' ')[0]
                # 如果key为none则跳过
                if searchStrs == 'none':
                    index += 1
                    continue
                # 按逗号分为标和class
                searchStrs = searchStrs.split(',')
                # --------------------------------
                l = self.__finder(searchStrs,browserList,index)
                # 如果值仍然是map则递归
                if isinstance(cmap[i],dict):
                    self.__find(cmap[i],l)
                else:
                    # 由于是末端部分所以不递归,保存搜索到的值
                    field = cmap[i]
                    if len(l) != 0:
                        self.__setInsert(field,self.__getSearchStr(l[0]))
                    else:
                        print(field+ ':出现错误,搜索不到足够数据')
                index += 1
    # 搜索子元素,如果为son则只查找子元素
    def __finder(self,searchStrs,browserList,index):
        # 没有class的情况
        if len(searchStrs) == 1 :
            if searchStrs[0] == 'son':
                l = browserList[index].find_all(recursive=False)
            elif searchStrs[0] == 'value':
                l = [browserList[index]]
            else:
                l = browserList[index].find_all(searchStrs[0])
        #有class的情况
        elif len(searchStrs) == 2:
            l = browserList[index].find_all(searchStrs[0],class_=searchStrs[1])
            if len(l) == 0:
                l = browserList[index].find_all(searchStrs[0],id=searchStrs[1])
                print(len(l))
        

        # --------------------------------
        return l
    def __setInsert(self,field,value):
        indexMap = self.insertMap
        #一个过滤,当叶端为过滤器时
        if isinstance(field,Ii):
            value = field.getVal(value)
            field = field.field
        # 如果field有空格隔开则进行分层
        fieList = field.split(' ')
        if len(fieList) > 1:
            if fieList[0] not in indexMap:
                indexMap[fieList[0]] = {}
            indexMap= indexMap[fieList[0]]
            field = fieList[1]          

        # 遇到同字段时自动转变为数组的机制
        # 当map没该键时:
        if field not in indexMap:
            indexMap[field] = value
        # 当该键是个list时
        elif isinstance(indexMap[field],list):
            indexMap[field].append(value)
        # 当有该键时,改为数组并录入
        else:
            w = indexMap[field]
            indexMap[field] =[w,value]
    def __getSearchStr(self,browser):
        if browser.string == None:
            a = str(browser).replace('<br/>','')
            context = BeautifulSoup(a, 'html.parser').string
            if context != None:
                rt = context.strip()
            else:
                rt = a
            return rt
        else:
            rt = browser.string.strip()
            return rt

"""
数据平面化模组
数据也用map进行操作:
- key表示数据源的字符串
- value表示要录入数据的field
"""
class DataChanger:
    def __init__(self,data):
        # 数据
        self.data = data
    def change(self,ruleMap = None,mapLan = 5):
        mydata = self.data
        rtList = []
        for i in range(mapLan):
            rtMap = {}
            # 如果无规则图则按照原map平面化
            if ruleMap != None:
                for k in ruleMap.keys():
                    # 取出值到返回的map上
                    if isinstance(ruleMap[k],list):
                        # 规则图的列表
                        valueList = ruleMap[k]
                        for j in range(len(valueList)):
                            rtMap[valueList[j]] = mydata[k][str(i)][j]
                    else:
                        rtMap[ruleMap[k]] = mydata[k][str(i)]
            else:
                for k in mydata.keys():
                    rtMap[k] = mydata[k][str(i)]
            rtList.append(rtMap)
        return rtList

# class DataInputer:
#     def __init__(self,user='dehm',password='normidar',db='dehm',host='127.0.0.1',port=3306):
#         self.db = pymysql.connect(host=host,port=port,user=user,password=password,db=db)
#         self.conn = self.db.cursor()
#     def insert(self,table,datas):
#         sql = self.__getInsertSql(table,datas[0])
#         self.conn.executemany(sql,datas)
#         self.db.commit()
#         self.db.close()
#     # update和上面的datas都是数组
#     def update(self,table,where,updates):
#         sql = self.__getUpdateSql(table,where,updates[0])
#         self.conn.executemany(sql,updates)
#         self.db.commit()
#         self.db.close()
#     def __getUpdateSql(self,table,where,data):
#         cols = ", ".join('{0}=%({0})s'.format(k) for k in data.keys())
#         # print(cols)  # '`name`, `age`'
#         for i in where.keys():
#             sql = "UPDATE "+ table +" SET %s WHERE "+i+ "="+ where[i]
#             break
#         res_sql = sql % (cols)
#         print(res_sql) # 'insert into users(`name`, `age`) values(%(name)s, %(age)s)'
#         return res_sql
#     def __getInsertSql(self,table,data):
#         cols = ", ".join('`{}`'.format(k) for k in data.keys())
#         # print(cols)  # '`name`, `age`'
#         val_cols = ', '.join('%({})s'.format(k) for k in data.keys())
#         # print(val_cols)  # '%(name)s, %(age)s'
#         sql = "insert into "+ table +"(%s) values(%s)"
#         res_sql = sql % (cols, val_cols)
#         # print(res_sql) # 'insert into users(`name`, `age`) values(%(name)s, %(age)s)'
#         return res_sql
    
#     @staticmethod
#     def createTableSql(table,data):
#         rt = "CREATE TABLE `" + table + "` (`id` int(11) unsigned NOT NULL AUTO_INCREMENT,"
#         for k in data.keys():
#             rt += "`"+k+"` int(11) DEFAULT NULL,"
#         rt += "PRIMARY KEY (`id`) ) ENGINE=InnoDB DEFAULT CHARSET=utf8;"
#         return rt
# DataInputer().update('abc',{'fie':'val'},{'a':'b','c':'d'})
# 末端过滤器的定义
class Ii:
    def __init__(self,field:str,func):
        self.field = field
        self.func = func
    def getVal(self,value):
        return self.func(value)