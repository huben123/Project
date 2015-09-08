# coding: utf-8
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib,sys  

reload(sys)
sys.setdefaultencoding('utf-8') 
 
mailto_list=["guoxuanma@163.com"] 
mail_host="smtp.163.com"  #设置服务器
mail_user="guoxuanma"    #用户名
mail_pass="1990829"   #口令 
mail_postfix="163.com"  #发件箱的后缀
  
def send_mail( sub, content,to_list=mailto_list):  #to_list：收件人；sub：主题；content：邮件内容
	#add attachment 
	# att2 = MIMEText(open('F:\MyCode\webdesign\demo.html', 'r').read(), 'base64', 'utf-8')
 #    att2["Content-Type"] = 'application/octet-stream'
 #    att2["Content-Disposition"] = 'attachment; filename="demo.html"'
 #    msg.attach(att2)
    
    me="glen"+"<"+mail_user+"@"+mail_postfix+">"   #这里的hello可以任意设置，收到信后，将按照设置显示
    msg = MIMEText(content,_subtype='html',_charset='gbk')    #创建一个实例，这里设置为html格式邮件
    msg['Subject'] = sub    #设置主题
    msg['From'] = me  
    msg['To'] = ";".join(to_list)  
    try:  
        s = smtplib.SMTP()  
        s.connect(mail_host)  #连接smtp服务器
        s.login(mail_user,mail_pass)  #登陆服务器
        s.sendmail(me, to_list, msg.as_string())  #发送邮件
        s.close()  
        return True  
    except Exception, e:  
        print str(e)  
        return False  

# if __name__ == '__main__':
#     reload(sys)
#     sys.setdefaultencoding('utf-8')    
#     if send_mail("hello","xiaofeima is very NB 信不信 ！！！！"):  
#         print "发送成功"  
#     else:  
#         print "发送失败"  
