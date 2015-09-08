# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 15:47:16 2015

@author: xiaofeima
"""

import sys as sys
import codecs
import xlrd,xlwt
import time, re
from datetime import date, timedelta,datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException
import selenium.common.exceptions as S_exceptions
import glob,os,copy
#driver = webdriver.Ie("IEDriverserver.exe")
# driver = webdriver.Firefox()

reload(sys)
sys.setdefaultencoding('utf-8')



def login_internet(driver):
    username = driver.find_element_by_id("username")
    password = driver.find_element_by_id("password")

    username.send_keys("2013101147")
    password.send_keys("mgx1990829")
    driver.find_element_by_id("loginBtn").click()



    return driver


def error_record_info(ID,url,thread_num,url_txt,num_line):
    error_file=open("error_record_info"+str(thread_num)+".txt","a+")
    error_file.write(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+"\n")
    error_file.write(u"ID|||"+str(ID)+"\n")
    error_file.write(u"href||| "+str(url))
    error_file.write(u"text_file||| "+str(url_txt)+"\n")
    error_file.write(u"num_line||| "+str(num_line)+"\n")
    error_file.write(u"---------------------------"+"\n")
    error_file.write(u"\n")
    error_file.close()

def error_recover(ID,thread_num):
    dict_error_info={"ID":"","href":"","text_file":"","num_line":""}
    error_file=open("error_record_info"+str(thread_num)+".txt","r")
    error_line=error_file.readline()
    while error_file !="":
        flag=0
        # extract the info
        end_line = re.findall(r"^ID", str(error_line))
        print end_line
        if len(end_line) :
            print error_line
            error_line=error_line.split("|||")
            print error_line
            if str(ID) in error_line[1] :
                while 1 : 
                    error_line=error_file.readline()
                    if error_line =="\n":
                        error_line=error_file.readline()
                    end_line = re.findall(r"---", str(error_line))
                    if len(end_line)>0:
                        flag=1
                        break
                    error_line=error_line.split("|||")
                    if len(error_line) :
                        print error_line
                        dict_error_info[error_line[0].strip()]=error_line[1].strip()
        if flag==1:
            break
        error_line=error_file.readline()

    return dict_error_info





list_content=[
        u"行政区",
        u"电子监管号",
        u"项目名称", 
        u"项目位置" ,
        u"面积(公顷)", 
        u"土地来源" ,
        u"土地用途" , 
        u"供地方式" ,  
        u"土地使用年限" ,
        u"行业分类", 
        u"土地级别", 
        u"成交价格(万元)" ,
        u"土地使用权人" , 
        u"约定容积率下限" ,
        u"约定容积率上限", 
        u"约定交地时间" ,
        u"约定开工时间",  
        u"约定竣工时间",
        u"批准单位",
        u"合同签定日期" ]

dic_content={
u"行政区":"mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r1_c2_ctrl",
u"电子监管号":"mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r1_c4_ctrl",
u"项目名称":"mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r17_c2_ctrl", 
u"项目位置":"mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r16_c2_ctrl" ,
u"面积(公顷)":"mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r2_c2_ctrl", 
u"土地来源":"mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r2_c4_ctrl" ,
u"土地用途":"mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r3_c2_ctrl" , 
u"供地方式": "mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r3_c4_ctrl",  
u"土地使用年限":"mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r19_c2_ctrl" ,
u"行业分类":"mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r19_c4_ctrl" , 
u"土地级别":"mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r20_c2_ctrl" , 
u"成交价格(万元)":"mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r20_c4_ctrl" ,
u"土地使用权人" :"mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r9_c2_ctrl", 
u"约定容积率下限":"mainModuleContainer_1855_1856_ctl00_ctl00_p1_f2_r1_c4_ctrl" ,
u"约定容积率上限":"mainModuleContainer_1855_1856_ctl00_ctl00_p1_f2_r1_c2_ctrl", 
u"约定交地时间" : "mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r21_c4_ctrl",
u"约定开工时间": "mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r22_c2_ctrl",  
u"约定竣工时间":"mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r22_c4_ctrl",
u"批准单位" :"mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r14_c2_ctrl",
u"合同签定日期":"mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r14_c4_ctrl", 
}



savefile=[]
savefile_date=[]
read_file_list=[]
read_file_list =os.listdir(".\\url\\")
#read_file_list = glob.glob('.\\url\\*.txt')
print read_file_list
for element in read_file_list:
    savefile.append(os.path.splitext(os.path.basename(element)))
    savefile_date.append(datetime.strptime(os.path.splitext(os.path.basename(element))[0],'%Y-%m-%d'))

#date_start=raw_input("Please enter spidder start date (YYYY-M-D,no zeros needed)?")
#link=open(date_start+".txt",'r')
#link_line=link.readline()
input_thread=raw_input("pseudo parallel: input thread NO. 1 2 3 4... ")
input_error_recover=raw_input("error recover 0=no, 1=yes ")
if input_error_recover=="1":
    error_ID=raw_input("input error ID")
else:
	date_start= raw_input("Please enter query start date (YYYY-M-D,no zeros needed)?")
	date_end=raw_input("Please enter query end date (YYYY-M-D,no zeros needed)?")
	print date_start,date_end
	date_start=datetime.strptime( date_start, '%Y-%m-%d')
	date_end=datetime.strptime( date_end, '%Y-%m-%d')




# normal running 
wait_file_date=[]
for element in savefile_date:
    if element >=date_start and element <= date_end: 
        wait_file_date.append(element)

# error recovering 
error_dict={}
if input_error_recover=="1":
    error_dict=error_recover(error_ID, input_thread)
    temp_path=datetime.strptime(error_dict["text_file"],'%Y-%m-%d')
    wait_file_date.append(temp_path)



while len(wait_file_date) > 0 :
    temp_file=wait_file_date.pop()

    temp_file=temp_file.strftime("%Y-X%m-X%d").replace('X0','X').replace('X','')
    print "now we are dealing with date: ", temp_file
    link=open(".\\url\\"+temp_file+".txt",'r')
    

    link_line=link.readline()

    count_url=0
    #print  driver.find_element_by_css_selector("td.pager").text
    #save_file=os.path.splitext(os.path.basename(temp_file))[0]
    if input_error_recover != "1" :
        data_export = codecs.open(".\\info\\"+temp_file+"export.txt",'w',"utf-8-sig")
        temp_line=""
        temp_line="\t".join(str(ele) for ele in list_content)
        temp_line=temp_line+"\t"+"url"
        temp_line=temp_line+"\n"
        data_export.write(temp_line)
        data_export.close()

    data_export = codecs.open(".\\info\\"+temp_file+"export.txt",'a+',"utf-8-sig")


    # wbk = xlwt.Workbook()
    # sheet = wbk.add_sheet('Sheet1')
        # for i in range(len(list_content)):
    #     sheet.write(0,i,list_content[i].decode("utf-8"))
    

    

    driver = webdriver.Ie("IEDriverserver.exe")
    try:
        
        while link_line != "":
            if link_line == "\n":
                link_line = link.readline()
            # locate
            if input_error_recover=="1":
                count_url=count_url+int(error_dict["num_line"])
                for i in range(1,int(error_dict["num_line"])+1):
                    link_line=link.readline()
                if error_dict["href"] in link_line :
                    print "locate the url !"
                    input_error_recover=0
                    print link_line
                else :
                    print "false, try again"
                    link.close()
                    link=open(".\\url\\"+temp_file+".txt",'r')
                    link_line=link.readline()
                    seach_flag=0
                    while seach_flag==0 and link_line !="":
                        if error_dict["href"] in link_line:
                            seach_flag=1
                            print "success!"
                            input_error_recover=0
                            break
                        link_line=link.readline()





            driver.get(link_line)
            # log_current_link=open("log-link"+str(input_thread)+".txt",'w')
            # log_current_link.write(str(link_line)+"\n")
            # log_current_link.write(str(temp_file)+"\n")
            # log_current_link.close()

            flag=0
            count=0
            while flag==0:
                
                try:
                    WebDriverWait(driver,30).until(EC.presence_of_element_located((By.ID,"mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r14_c4_ctrl")))
                    time.sleep(1)
                    flag=1
                    count=count+1
                except:
                    if "a70.htm" in str(driver.current_url):
                        driver=login_internet(driver)
                        time.sleep(10)
                        driver.get(link_line)
                    try : 
                        WebDriverWait(driver,30).until(EC.presence_of_element_located((By.ID,"mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r14_c4_ctrl")))
                        time.sleep(1)
                        flag=1
                        count=count+1
                    except S_exceptions.NoSuchWindowException as e:
                        print "check your internet "
                        driver=login_internet(driver)
                        time.sleep(10)
                        driver.get(link_line)


                
                if flag==1:
                    break
                if count>5:
                    print "can not open this page error"
                    error_record_info(input_thread, link_line, input_thread, temp_file,count_url)

                    break
            
            
            if count>5:
                continue
            
            temp_list_data={}

            for name, ID_element in dic_content.items():
                try:
                    temp_list_data[name]=driver.find_element_by_id(ID_element).text
                except:
                    temp_list_data[name]=""
                print name, u":" ,  
                try:
                    print temp_list_data[name].decode('utf-8','ignore')
                except :
                    pass


            # print u"-------------------------------------"

            data_list={}
            data_list=copy.deepcopy(temp_list_data)
            # for j in range(len(list_content)):
                # temp = data_list[list_content[j]]
                # sheet.write(i+1,j,temp.decode("utf-8"))
            
            writeline="\t".join(data_list[list_content[j]] for j in range(len(list_content)))
            writeline=writeline+"\t"+str(link_line).rstrip()
            writeline=writeline+"\n"
            # writeline =ID_num+","+xzq+","+dzjgh+","+xmwz+","+mj_gq+","+tdly+","+tdyt+","+gdfs+","+tdsynx+","+hyfl+","+tdjb+","+cjjg+","+tdsyqr+","+rjlsx+","+rjlxx+","+htqdrq+","+"\n"
            data_export.write(writeline.encode("utf-8-sig"))
            print u"<--------------!-------------->"
            link_line = link.readline()
            count_url=count_url+1

        link.close()
        data_export.close()
        driver.close()
    except :
        print "error occured "
        link.close()
        data_export.close()
        error_record_info(input_thread, link_line, input_thread, temp_file,count_url)
        driver.close()


driver.close()
driver.quit()