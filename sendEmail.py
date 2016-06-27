# -*- coding: utf-8 -*-
import smtplib
import email.MIMEMultipart# import MIMEMultipart
import email.MIMEText# import MIMEText
import email.MIMEBase# import MIMEBase
import os.path
import mimetypes
import time

From = "tangwen@dobest.com"
To = "xxx@163.com"
dateStr = time.strftime("%Y-%m-%d", time.localtime(time.time()))
file_name = "C:\Users\Thinkpad\Desktop\dailyFiles" + "\\" + dateStr + "\work.txt"
print file_name


server = smtplib.SMTP_SSL("smtp.exmail.qq.com", 465)
server.login(From,"xxx") #仅smtp服务器需要验证时

# 构造MIMEMultipart对象做为根容器
main_msg = email.MIMEMultipart.MIMEMultipart()

# 判断是否是空内容
file_context = open(file_name).read().strip()
if (file_context == 'today work is:'):
    # 相当于内容为空，给自己发一份提示邮件
    text_msg = email.MIMEText.MIMEText("你今日的工作情况还未做记录，请检查后手动运行该脚本发送邮件。",_charset="utf-8")
    main_msg.attach(text_msg)
    main_msg['From'] = From
    main_msg['To'] = From
    main_msg['Subject'] = "今日工作汇报发送失败"
    main_msg['Date'] = email.Utils.formatdate()
    # 得到格式化后的完整文本
    fullText = main_msg.as_string( )
    # 用smtp发送邮件
    try:
        server.sendmail(From, From, fullText)
    finally:
        print 'success!'
        server.quit()

    print u"你今日的工作情况还未做记录，请检查后手动运行该脚本发送邮件。"
    exit()


# 构造MIMEText对象做为邮件显示内容并附加到根容器
text_msg = email.MIMEText.MIMEText("你好，今日的工作情况见附件",_charset="utf-8")
main_msg.attach(text_msg)

# 构造MIMEBase对象做为文件附件内容并附加到根容器

## 读入文件内容并格式化 
data = open(file_name, 'rb')
ctype,encoding = mimetypes.guess_type(file_name)
if ctype is None or encoding is not None:
    ctype = 'application/octet-stream'
maintype,subtype = ctype.split('/',1)
file_msg = email.MIMEBase.MIMEBase(maintype, subtype)
file_msg.set_payload(data.read())
data.close( )
email.Encoders.encode_base64(file_msg)#把附件编码

## 设置附件头
basename = os.path.basename(file_name)
file_msg.add_header('Content-Disposition','attachment', filename = basename)#修改邮件头
main_msg.attach(file_msg)

# 设置正文内容
# # 设置根容器属性
main_msg['From'] = From
main_msg['To'] = To
main_msg['Subject'] = "今日工作汇报"
main_msg['Date'] = email.Utils.formatdate()

# 得到格式化后的完整文本
fullText = main_msg.as_string( )

# 用smtp发送邮件
try:
    server.sendmail(From, To, fullText)
finally:
    print 'success!'
    server.quit()
