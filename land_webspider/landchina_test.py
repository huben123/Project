
# coding: utf-8

# #Test for Selenium in landchina.com 
# aim at scrapying the first market data 
# using firfox first 
# Charactors: 
# 1 automatic select time period to show the info 
# 2 pagenate 
# 3 

# In[1]:

import sys as sys
import codecs
import time, re, copy
from datetime import date, timedelta,datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException
import selenium.common.exceptions as S_exceptions
import python_email as e_email
driver = webdriver.Ie("IEDriverserver.exe")
# driver = webdriver.Firefox()


# In[2]:
input_thread=raw_input("pseudo parallel: input thread NO. 1 2 3 4 ")
input_flag=raw_input( "make a choice : input the (1)starting date or (0)monthly automatic select or (2) error recover")
if input_flag=="0":
    print "prepareing for the monthly spider"
    date_start=raw_input("Please enter start month yyyy-m:")
    date_end  =raw_input("Please enter end month yyyy-m:")
elif input_flag=="1": 
    date_start= raw_input("Please enter query start date (YYYY-M-D,no zeros needed)?")
    date_end=raw_input("Please enter query end date (YYYY-M-D,no zeros needed)?")
else:
    print "first recover the error"
    error_ID=raw_input("input error ID")
    error_end_date=raw_input("input error end date (YYYY-M-D,no zeros needed)")
    date_start= raw_input("Please enter query start date (YYYY-M-D,no zeros needed)?")
    date_end=raw_input("Please enter query end date (YYYY-M-D,no zeros needed)?")



day_interval=10
writeline=""
if input_flag=="1":
    print date_start,date_end
    date_start=datetime.strptime( date_start, '%Y-%m-%d')
    print "this is datetime format", date_start.strftime("%Y-X%m-X%d").replace('X0','X').replace('X','')
    date_end=datetime.strptime( date_end, '%Y-%m-%d')
elif input_flag=="0":
    print date_start,date_end
    date_start=datetime.strptime( date_start, '%Y-%m')
    print "this is datetime format", date_start.strftime("%Y-X%m").replace('X0','X').replace('X','')
    date_end=datetime.strptime( date_end, '%Y-%m')
else:
    date_start=datetime.strptime( date_start, '%Y-%m-%d')
    date_end=datetime.strptime( date_end, '%Y-%m-%d')
    error_end_date=datetime.strptime(error_end_date, '%Y-%m-%d')


# In[3]:

def open_page(driver,url,temp_date1,temp_date2):
    driver.get(url)
    driver.implicitly_wait(10)
    driver.find_element_by_id("TAB_QueryConditionItem270").click()
    driver.find_element_by_id("TAB_queryDateItem_270_1").click()
    driver.find_element_by_id("TAB_queryDateItem_270_1").send_keys(temp_date1.strftime("%Y-X%m-X%d").replace('X0','X').replace('X',''))
    driver.find_element_by_id("TAB_queryDateItem_270_2").click()
    driver.find_element_by_id("TAB_queryDateItem_270_2").send_keys(temp_date2.strftime("%Y-X%m-X%d").replace('X0','X').replace('X',''))
    driver.find_element_by_id("TAB_QueryButtonControl").click()
    time.sleep(3)
    return driver


# In[8]:

def makesure_page(driver,url,temp_date1,temp_date2,try_times=10):
    
    driver=open_page(driver,url,temp_date1,temp_date2)
    time.sleep(10)
    index_flag=1
    while (try_times > 0):
        try_times=try_times-1
        try:
            WebDriverWait(driver,60).until(EC.presence_of_element_located((By.CSS_SELECTOR,"td.pager")))
            index_flag=0

            if len(driver.find_elements_by_xpath("//*[contains(text(), '没有检索到相关数据')]"))> 0:
                print "input wrong date,please restart again "
                sys.exit(0)

        except S_exceptions.ErrorInResponseException as e:
            index_flag=1
            print "No response please try again, make sure you connect the Internet "

        except :
            index_flag=1
            print "Unexpected error:", sys.exc_info()[0]
            print "please wait"

        if index_flag==0 :
            print "page succeed"
            break

        if try_times==0 :
            print "fatal error, can't connect to Landchina.com,Please try again later"
            sys.exit(0)
    return driver


# In[11]:

def execute_link(driver, i, check_flag,url,temp_date1,temp_date2):
    driver.execute_script("QueryAction.GoPage('TAB',"+str(i)+",200)")
    time.sleep(10)
    flag=0
    while flag==0:
        data_check=""
        try:
            WebDriverWait(driver,60).until(EC.presence_of_element_located((By.CSS_SELECTOR,"td.pager")))
            data_check=driver.find_element_by_css_selector("td.pager").text
        except  S_exceptions.InvalidSelectorException as e:
            print e, "try again"
            driver.execute_script("QueryAction.GoPage('TAB',"+str(i)+",200)")
            time.sleep(10)
        except  :
            print "try again strat from beginning"
            print "Unexpected error:", sys.exc_info()[0]
            driver.close()
            driver = webdriver.Ie("IEDriverserver.exe")
            driver=makesure_page(driver,url,temp_date1,temp_date2)
            time.sleep(10)
            driver.execute_script("QueryAction.GoPage('TAB',"+str(i)+",200)")
            time.sleep(10)
        
        if data_check == check_flag :
            try : 
                num_link=driver.find_elements_by_xpath("/html/body/form/font/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/a")
                flag=1
            except :
                driver.execute_script("QueryAction.GoPage('TAB',"+str(i)+",200)")
                time.sleep(10)
                
        else: 
            driver=makesure_page(driver,url,temp_date1,temp_date2)
            driver.execute_script("QueryAction.GoPage('TAB',"+str(i)+",200)")
            time.sleep(10)   
    return num_link


# record error information 
def error_record(ID,start_date,end_date,num_page,thread_num):
    error_file=open("error_record_url"+str(thread_num)+".txt","a+")
    
    start_date=start_date.strftime("%Y-%m-%d")
    end_date=end_date.strftime("%Y-%m-%d")
    error_file.write(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+"\n")
    error_file.write(u"ID|||"+str(ID)+"\n")
    error_file.write(u"start_date|||"+str(start_date)+"\n")
    error_file.write(u"end_date|||"+str(end_date)+"\n")
    error_file.write(u"num_page|||"+str(num_page)+"\n")
    error_file.write(u"----------------------------"+"\n")
    print "error record "

def error_recover(ID,thread_num):
    dict_error_info={"ID":"","start_date":"","end_date":"","num_page":""}
    error_file=open("error_record_url"+str(thread_num)+".txt","r")
    error_line=error_file.readline()
    while error_file !="":
        # extract the info
        error_line=error_file.readline()
        
        end_line = re.findall(r"---", str(error_line))
        if len(end_line)>0:
            break
        error_line=error_line.split("|||")
        dict_error_info[error_line[0]]=error_line[1].strip()
        
            

    return dict_error_info





# In[15]:

# start to split time date
def catch_url(driver, url, temp_date1, temp_date2, date_end, start_point=1 ):
    while (temp_date2 <= date_end):
        
        data_confirm="n"
        day_interval=10
        while data_confirm != "y":
                   
            driver=makesure_page(driver,url,temp_date1,temp_date2)
            flag=0
            while flag==0:
                
                try: 
                    data_summary=driver.find_element_by_css_selector("td.pager").text
                    flag=1
                except :
                    print "error in finding element"
                    driver=makesure_page(driver,url,temp_date1,temp_date2)
                    time.sleep(5)
                
                if flag==1:
                    print "get the info"
                    break     
            
            print "#"+data_summary+"#"
            page_info=re.findall("[-+]?\d+[\.]?\d*", data_summary)
            num_page= page_info[0]
            total_record=page_info[-1]
            # check the number of pages 
            if int(num_page) <= 200:
                data_confirm ="y"
            else :
                
                temp_date2=temp_date2-timedelta(days=int(day_interval/2))
                if temp_date2<temp_date1 :
                    print "error, the information is too big, we need to start with day by day "
                    temp_date2=temp_date1+timedelta(days=1)
                
    #------------------------------------------------------------------------------------------------------------------------------------------#
    # next part is to scrap the url link 
    #------------------------------------------------------------------------------------------------------------------------------------------#
        print "current date range is :",str(temp_date1)+"---"+str(temp_date2)
        data_pages=int(data_summary[data_summary.index(u'共')+1:data_summary.index(u'页')])
        file_name =temp_date1.strftime("%Y-X%m-X%d").replace('X0','X').replace('X','')
        if start_point== 1 :
            write_format='w'
        else :
            write_format='a+'


        export =codecs.open(".\\url\\"+file_name+".txt",write_format,"utf-8")

        
            # log record
        try:  
            for i in range(start_point,data_pages+1):
                href_flag=0
                while href_flag==0: 
                    num_link=execute_link(driver, i, data_summary,url,temp_date1,temp_date2)
                    href_flag=1
                    print i,len(num_link)
                    for record in num_link:
                        try:
                            writeline=record.get_attribute("href")+"\n"
                            export.write(writeline)
                        except :
                            print "an unget link"
                            href_flag=0
                            break
        except :
            print "record the error"
            error_record(input_thread, temp_date1, temp_date2, i, input_thread)
            export.close()
            e_email.send_mail("error in catching url!","an error happens")
                # driver.close()

            

        export.close()  
        
    #------------------------------------------------------------------------------------------------------------------------------------------#    
        # judge the time period
        start_point=1
        temp_date1 = temp_date2+timedelta(days=1)
        temp_date2=temp_date1+ timedelta(days=10)
        if temp_date1 <= date_end and temp_date2 > date_end:
            temp_date2=date_end
    
    
    driver.close()
    driver.quit()
    




url ="http://www.landchina.com/default.aspx?tabid=263&ComName=default"
if input_flag=="1":
    total_days=date_end - date_start
    total_days=int(total_days.days)+1
    print "total date range : ",date_start,"--", date_end
    print "total days: " + str(total_days)
    temp_date1=date_start
    temp_date2=temp_date1+ timedelta(days=10)
    if temp_date2 > date_end:
        temp_date2=date_end
    catch_url(driver, url, temp_date1, temp_date2, date_end)
elif input_flag=="0":
    temp_year=date_start.year
    end_month=date_end.month
    temp_start_month=date_start.month
    while temp_start_month < end_month:
        temp_start_day=date(temp_year, temp_start_month,1)
        if temp_start_month+1 <=12: 
            temp_end_day=date(temp_year, temp_start_month+1,1)-timedelta(days=1)
        else:
            temp_end_day=date(temp_year+1,1,1)-timedelta(days=1)
            
        temp_date1=temp_start_day
        temp_date2=temp_date1+ timedelta(days=10)
        if temp_date2 > temp_end_day:
            temp_date2=temp_end_day
        catch_url(driver, url, temp_date1, temp_date2, temp_end_day)
        
        temp_start_month=temp_start_month+1
else :
    dict_error_info={}
    print "error ID = ",error_ID,"thread =", input_thread
    dict_error_info=error_recover(error_ID, input_thread)
    # start recovering
    print "recovering the error "
    for name, ele in dict_error_info.items() :
        try :
            print name.encode("utf-8","ignore"), ":", ele.encode("utf-8","ignore")
        except :
            pass
    err_start_date=datetime.strptime(dict_error_info["start_date"], '%Y-%m-%d')
    err_end_date=datetime.strptime(dict_error_info["end_date"], '%Y-%m-%d')
    num_page=int(dict_error_info["num_page"])
    catch_url(driver, url, err_start_date, err_end_date, error_end_date,num_page)

    # for a new starter 
    total_days=date_end - date_start
    total_days=int(total_days.days)+1
    print "total date range : ",date_start,"--", date_end
    print "total days: " + str(total_days)
    temp_date1=date_start
    temp_date2=temp_date1+ timedelta(days=10)
    if temp_date2 > date_end:
        temp_date2=date_end
    catch_url(driver, url, temp_date1, temp_date2, date_end)


e_email.send_mail("finish and succeed", "The program is ok for you")



        




#
##------------------------------------------------------------------------------
## scrapy the info
##------------------------------------------------------------------------------
#import glob
#read_file_list = glob.glob('E:\\guoxuanma\\webspider\\url\\*.txt')
#
#
##date_start=raw_input("Please enter spidder start date (YYYY-M-D,no zeros needed)?")
##link=open(date_start+".txt",'r')
##link_line=link.readline()
#while len(read_file_list) > 0 :
#    temp_file=read_file_list.pop()
#    link=open(temp_file,'r')
#    
#
#    link_line=link.readline()
#    #print  driver.find_element_by_css_selector("td.pager").text
#    save_file=os.path.splitext(os.path.basename(temp_file))[0]
#    data_export = codecs.open("F:\\RD\\develop\\python\\webspider\\info\\"+save_file+"export.csv",'w',"utf-8")
#    driver = webdriver.Firefox()
#    while link_line != "":
#        if link_line == "\n":
#            link_line = link.readline()
#
#        driver.get(link_line)
#
#
#        try:
#            WebDriverWait(driver,30).until(EC.presence_of_element_located((By.ID,"mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r14_c4_ctrl")))
#        except:
#            driver.refresh()
#          
#        
#
#        print u'行政区：',
#        xzq = driver.find_element_by_id("mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r1_c2_ctrl").text
#        print xzq
#        print u'电子监管号：',
#        dzjgh = driver.find_element_by_id("mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r1_c4_ctrl").text
#        print dzjgh
#        print u'项目位置:',
#        xmwz = driver.find_element_by_id("mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r16_c2_ctrl").text
#        try:
#            print xmwz
#        except:
#            print ""
#
#        print u'面积_公顷:',
#        mj_gq = driver.find_element_by_id("mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r2_c2_ctrl").text
#        print mj_gq
#        print u'土地来源:',
#        tdly = driver.find_element_by_id("mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r2_c4_ctrl").text
#        print tdly
#        print u'土地用途:',
#        tdyt = driver.find_element_by_id("mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r3_c2_ctrl").text
#        print tdyt
#        print u'供地方式:',
#        gdfs = driver.find_element_by_id("mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r3_c4_ctrl").text
#        print gdfs
#
#        print u'土地使用年限:',
#        tdsynx = driver.find_element_by_id("mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r19_c2_ctrl").text
#        print tdsynx
#        print u'行业分类:',
#        hyfl = driver.find_element_by_id("mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r19_c4_ctrl").text
#        print hyfl
#        print u'土地级别:',
#        tdjb = driver.find_element_by_id("mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r20_c2_ctrl").text
#        print tdjb
#        print u'成交价格:',
#        cjjg = driver.find_element_by_id("mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r20_c4_ctrl").text
#        print cjjg
#        print u'土地使用权人:',
#        tdsyqr = driver.find_element_by_id("mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r9_c2_ctrl").text
#        try:
#            print tdsyqr
#        except:
#            print ""
#
#        print u'容积率上限:'
#        try :
#            rjlsx = driver.find_element_by_id("mainModuleContainer_1855_1856_ctl00_ctl00_p1_f2_r1_c4_ctrl").text
#        except :
#            print sys.exc_info()[0]
#            rjlsx = ""   
#        print rjlsx
#        print u'容积率下限'
#        try :
#            rjlxx = driver.find_element_by_id("mainModuleContainer_1855_1856_ctl00_ctl00_p1_f2_r1_c2_ctrl").text
#        except :
#            print sys.exc_info()[0]
#            rjlsx = ""
#        print u'合同签订日期:',
#        htqdrq = driver.find_element_by_id("mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r14_c4_ctrl").text
#        print htqdrq
#
#        writeline = xzq+","+dzjgh+","+xmwz+","+mj_gq+","+tdly+","+tdyt+","+gdfs+","+tdsynx+","+hyfl+","+tdjb+","+cjjg+","+tdsyqr+","+rjlsx+","+rjlxx+","+htqdrq+","+"\n"
#        data_export.write(writeline)
#        link_line = link.readline()
#    link.close()
#    data_export.close()
#
#driver.close()
#driver.quit()