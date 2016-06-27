# -*- coding: utf-8 -*-
import os
import datetime
date = datetime.datetime.now().strftime("%Y-%m-%d")
path = 'C:/Users/Thinkpad/Desktop/dailyFiles'
dailyPath = path + '/' + date


# 获取十天前的时间字符串
#tenDayAgo = (datetime.datetime.now() - datetime.timedelta(days = 10)).strftime("%Y-%m-%d")


###
# shutil.move(src_path, dst_path)
# 每过十天为一组，将之前的文件夹移到新文件夹里
###
if os.path.isdir(path) == False:
    os.mkdir(path)
    print("create dailyFiles folder success!")
if os.path.isdir(dailyPath) == False:
    os.mkdir(dailyPath)
    print("create %s folder success!" %date)

for filename in ['work', 'reading', 'novel', 'tech_arti']:
    if os.path.isfile( dailyPath + '/' + filename + '.txt') == False:
        with open(dailyPath + '/' + filename + '.txt','w') as f:
            f.write('today %s is:\n' %filename)
            print("create " + date + " of %s file success!" % filename)

