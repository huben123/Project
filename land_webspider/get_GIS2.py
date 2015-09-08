
# coding: utf-8

# # 土地经纬度信息获取
# 
# * 依靠百度地图API接口获得一级、二级市场数据经纬度信息
# * 载入地址和行政区数据
# * 规整好API接口与调用函数
# * 查找GIS信息
# * 数据规整
# 
# 

# In[2]:

import pandas as pd
import numpy as np
import sys 
# from pandas import Series,DataFrame
import urllib
import hashlib
import requests
import math
import re
import json
import copy


# ## GIS查询函数
# 
# * 利用map模式进行api数据查询

# In[1]:

def baidu_gis(queryStr):
    '''
    queryStr 包括了请求百api的url 地址
    以get请求为例http://api.map.baidu.com/geocoder/v2/?address=百度大厦&output=json&ak=yourak
    并且对url 转码 除了保留字符不转换，其余要进行转码加密
    
    '''
    
    GIS_result=[]
    api_link=[]
    error_count=0
    # 对queryStr进行转码，safe内的保留字符不转换
    for ele in queryStr:
        encodedStr=urllib.quote(ele, safe="/:=&?#+!$,;'@()*[]")
        # 在最后直接追加上yoursk
        rawStr = encodedStr + 'DTtxldoesco94o9YZT3RuGlKarBGr7Xv'

        sn = hashlib.md5(urllib.quote_plus(rawStr)).hexdigest()

        api_link.append('http://api.map.baidu.com'+ele+"&sn="+sn)
        
        
    
    req = map(requests.get,api_link)
    for ele in req:
        
        content = json.loads(ele.content)
        try: 
            result = content['result']
            location = result['location']
            x = location['lat']
            y = location['lng']
            temp_result=(x,y,result['confidence'])
            GIS_result.append(copy.deepcopy(temp_result))

        except: 
            temp_result=("","","")
            GIS_result.append(copy.deepcopy(temp_result))
            error_count +=1 
            print error_count
#             print content
    
    GIS_df=pd.DataFrame(GIS_result,columns=['lat','lng','confidence'])
    return GIS_df


# ## 市场经纬度获取

# **导入数据**
# 
# 打开HDF5数据库提取二级市场的clean data 

# In[3]:

path = "F:\\DATAbase\\land\\HDF\\" 
with pd.HDFStore(path+'LandDATA.h5',  mode='r') as store:
    print store.keys
    fm_df=store.get('fm_industry')
    sm_df=store.get('sm_industry')



# **构建待输入的查询字符串**
# 
# 

# In[ ]:

# construct the query data 

##########
#二级市场 #
##########
query_add =u'/geocoder/v2/?address='
query_city =u'&city='
query_suffix=u'&output=json&ak=9gTAEoFWvBoKHl3u3dFp5ff7'
query_sm =query_add+sm_df[u'地址']+query_city+sm_df[u'县']+"&province="+sm_df[u'省']+query_suffix
query_sm.fillna("",inpalce=True)
query_sm=query_sm.str.encode('utf-8')


##########
#一级市场 #
##########
query_add =u'/geocoder/v2/?address='
query_city =u'&city='
query_suffix=u'&output=json&ak=9gTAEoFWvBoKHl3u3dFp5ff7'
query_fm =query_add+fm_industry['项目位置'].str.decode('utf-8')+query_city+fm_industry['行政区'].str.decode('utf-8')+query_suffix
# query_sm=query_sm.str.encode('utf-8')
query_sm.fillna("",inpalce=True)
query_fm.str.encode('utf-8')


# **获取二级市场经纬度信息**
# 
# * 转存为dataframe结构，构建子dataframe

# In[ ]:

###
# get the result 二级市场
###
# %debug
GIS_df=baidu_gis(query_sm)
print GIS_df.shape # total number 


## get how many empty GIS
print "the num of empty GIS is : ",
print len(GIS_df[GIS_df['lat']==""])

## save the result in the total info data
cand_col_sm=['mkey_1',u'县',u'地址',u'剩余年限',u'面积',u'转让费)',u'容积率']
sm_GIS=pd.concat([sm_industry[cand_col_sm],GIS_df],axis=1)





# In[ ]:



###
# get the result  一级市场
###
# %debug
GIS_df=baidu_gis(query_fm)
print GIS_df.shape # total number 


## get how many empty GIS
print "the num of empty GIS is : ",
print len(GIS_df[GIS_df['lat']==""])

## save the result in the  data
cand_col_fm=['mkey_1',u'行政区',u'项目位置',u'土地使用年限',u'面积(公顷)',u'成交价格(万元)',u'约定容积率上限']
sm_GIS=pd.concat([sm_industry[cand_col_fm],GIS_df],axis=1)


# ## 保存数据

# In[ ]:

##------------------
##  save the data 
##------------------
path = "F:\\DATAbase\\land\\HDF\\"
with pd.HDFStore(path+'LandDATA.h5',  mode='w') as store:
    print store.keys
    store.put('sm_GIS',  sm_GIS,  format='f',append=False)
    store.put('fm_GIS', fm_GIS, format='f',append=False)


# # 附录

# In[ ]:

# fm_industry.columns
# fm_industry['行政区']
# fm_industry['行政区'].fillna('',inplace=True)

# data_sm[u'县'].fillna('',inplace=True)
# data_sm[u'市'].fillna('',inplace=True)
# fm_industry['项目位置'].str.decode('utf-8').str.encode('utf-8') 
fm_industry['行政区'].str.decode('utf-8').str.encode('utf-8')


# In[ ]:

## test for json file 
queryStr=query_sm[1:100]
GIS_result=[]
api_link=[]
error_count=0
# 对queryStr进行转码，safe内的保留字符不转换
for ele in queryStr:
    encodedStr=urllib.quote(ele, safe="/:=&?#+!$,;'@()*[]")
    # 在最后直接追加上yoursk
    rawStr = encodedStr + 'DTtxldoesco94o9YZT3RuGlKarBGr7Xv'

    sn = hashlib.md5(urllib.quote_plus(rawStr)).hexdigest()

    api_link.append('http://api.map.baidu.com'+ele+"&sn="+sn)



req = map(requests.get,api_link)

for ele in req:
    content = json.loads(ele.content)
    try: 
        result = content['result']
        location = result['location']
        x = location['lat']
        y = location['lng']
        temp_result=(x,y,result['confidence'])
        GIS_result.append(copy.deepcopy(temp_result))

    except: 
        temp_result=("","","")
        GIS_result.append(copy.deepcopy(temp_result))
        error_count +=1 
        print error_count

pd.DataFrame(GIS_result,columns=['lat','lng','confidence'])

