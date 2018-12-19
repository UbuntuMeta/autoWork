# coding=utf8
"""
针对http://api.mobimedical.cn的数据字典自动化发布新文档

author tonny<fightforphp@gmail.com>


curl命令实现：
curl --cookie "PHPSESSID=b1ce8b1a94718f1b4803d9938f833021;cookie_token=942b83ca84f69488a2a96c138fb92a6b" \
 -d "page_id=&cat_id=297&s_number=&page_content=test2w3223&page_title=mytry2&page_comments=&item_id=32" \
http://api.mobimedical.cn/index.php?s=home/page/save

思路：
 1.登录一次后获取了cookie_token
 2.组装好数据发送请求
 3.记录已写入的数据文档记录，防止多次运行导致重复生成的问题。
 4.对失败post做记录。 写入文件吧

 todo 拓展成多线程 （了解一下python多线程
"""
import requests
import random
import pymysql
import json, string
def post_article():
    post_url = 'http://api.mobimedical.cn/index.php?s=home/page/save';
    user_agents = [
            'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
            'Opera/9.25 (Windows NT 5.1; U; en)',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
            'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
            'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
            'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
            "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
            "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 ",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
    ]
    agent = random.choice(user_agents)
    # 获取提交数据
    add_posts = ['merit_vote','merit_vote_user','model_user', 'patient_illtype', 'report_health', 'role_privilege', 'schedule', 'scheduleDuty', 'scheduleDutyTag',
                 'scheduleGroup', 'scheduleLog', 'scheduleUser', 'sign']
    add_posts = ['scheduleGroup', 'scheduleLog', 'scheduleUser', 'sign', 'smartAppStep', 'smartAppStatement', 'smartAppDataRef', 'ivf_hand_history']
    add_posts = ['ivf_hand_history']
    for article in add_posts:
        f = open('E:/pythonwork/autoWork/turnMarkdown/markdownfiles/' + article + '.txt', 'r', encoding='utf-8')
        print('prepare insert article is:%s\n', article)

        content = f.read()
        page_title = article + 's'
        f.close()
        post_data = {'cat_id': '297', 'page_content': content, 'page_title': page_title, 'item_id': '32'}
        print(post_data)
        # cookie的一种设置方法 设置成cookie为headers里面的一个设置
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': agent,
        }
        # 'Cookie': 'PHPSESSID=b1ce8b1a94718f1b4803d9938f833021; cookie_token=942b83ca84f69488a2a96c138fb92a6b'

        # cookie也可以使用第三个参数进行传递
        cookies = {'cookie_token': '942b83ca84f69488a2a96c138fb92a6b', 'PHPSESSID': 'b1ce8b1a94718f1b4803d9938f833021'}
        print(headers)
        result = requests.post(post_url, data=post_data, headers=headers,
                               cookies=cookies)  # 第二种方法就是如此，把cookies作为一个参数传给post方法，get方法类似
        # cookies = {'name1': 'cookie1', 'name2': 'cookies2'}
        # # cookies=dict(name1='cookie1',name2='cookies2')
        # r = requests.get(url, cookies=cookies)
        # print(r.status_code)
        print(result.text)
        result_dict = json.loads(result.text)
        # {"error_code": 0,
        #  "data": {"page_id": "1890", "author_uid": "289", "author_username": "fightforphp@gmail.com", "item_id": "32",
        #           "cat_id": "297", "page_title": "testmemoke", "page_content": "\u6211\u5c31\u60f3\u6d4b\u8bd5\u4e00\u4e0b",
        #           "s_number": "99", "addtime": "1541301270", "page_comments": ""}}
        print(type(result_dict))  # 检查不是字典
        if result_dict['error_code'] == 0:
            print("prepare to insert\n")
            result_data = result_dict['data']
            post_id = result_data['page_id']
            model_name = result_data['page_title']
            created = result_data['addtime']
            db = pymysql.connect('192.168.99.100', 'root', '1234567qaz', 'post_emt_log')
            cursor = db.cursor()
            sql = "INSERT INTO post(post_id,model_name, created) \
                       VALUES ('%d', '%s', '%d' )" % \
                  (int(post_id), model_name, int(created))
            try:
                print("insert sql is:\n")
                print(sql)
                # 执行sql语句
                cursor.execute(sql)
                # 执行sql语句
                db.commit()
                print("success insert!")
            except Exception as e:
                # 发生错误时回滚
                print("some error\n")
                raise e
                db.rollback()
                db.close()


post_article()

# 用于删除测试数据
def remove_post(page_id):
    delete_url = 'http://api.mobimedical.cn/index.php?s=/home/page/delete/page_id/' + str(page_id)
    print(delete_url)
    cookies = {'cookie_token':'942b83ca84f69488a2a96c138fb92a6b', 'PHPSESSID': 'b1ce8b1a94718f1b4803d9938f833021'}
    res = requests.get(delete_url, cookies=cookies)
    print(res.text)


#remove_post(1883)