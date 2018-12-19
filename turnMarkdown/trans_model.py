"""
author tonny<fightforphp@gmail.com>
python实现自动化生成markdown格式的文档

思路
根据规则解析出字段等信息，然后生成markdown文档。

步骤
1.读取model文件内容。
2.解析需要内容到list.
3.拼装。
4.写入文件。

todo 考虑实现批量和自动。
"""
import re, os, sys
sys.path.append('./libs')
from file_tool import  get_file_name_from_path #scriptName without .py extension

def getSchemaPart(file_path, new_file_path):
    content = []
    model_file = open(file_path, 'r', encoding='utf-8')
    pure_content = model_file.read()
    if pure_content.index('{type') > -1:
        # 则是新写法 {type: xxxxx}
        pass
    # 利用正则匹配获取model中field定义部分
    ret = re.findall(r'Schema\({(.*)}, { versionKey: false }\)', pure_content, re.I|re.S)
    #print(ret[0])
    print(ret)
    if (len(ret) == 0): # 为了兼容一些model定义写法的不同，避免无法正则匹配出需要的部分
        ret = re.findall(r'Schema\({(.*)},{versionKey: false}\)', pure_content, re.I|re.S)
    print(ret)
    # 针对stl部分定义和其他不同的model进行处理
    if len(ret) == 0:
        ret = re.findall(r'Schema\({(.*)}\);', pure_content, re.I | re.S)

    if (len(ret) == 0):
        return 0
    str = ret[0]

    new_file = open(new_file_path, 'w', encoding='utf-8')
    new_file.write(str)
    new_file.close()
    f = open(new_file_path, 'r', encoding='utf-8')
    while 1:
        line = f.readline()
        if not line:
            break
        line = line.strip()
        if not len(line) or line.startswith('//'): # 去掉空白行和注释行
            continue
        content.append(line)
    f.close()
    os.remove(new_file_path) # 删除临时文件
    new_content = []

    for line in content:
        # 先删除被注释的行内容
        current_line = '|'
        if line.find('//') > 0:
            # print(line)
            # exit(0)
            annotation_part = line.split('//')
            # 无注释部分 记得判断最后是否是逗号分隔，如果没有，则说明是最后一行
            no_anno = annotation_part[0]
            #print(no_anno + "\r")
            no_anno = no_anno .replace('\t', '')
            no_anno = no_anno.replace(':', '  |  ')
            if not no_anno.endswith(','):
                no_anno += ','
            else:
                pass
                #print('not the end\r')
            no_anno = no_anno.replace(',', '')
            current_line += no_anno
            # 有注释部分
            anno =  '| ' + annotation_part[1]
            #print(anno)
            current_line += anno + ' |\n '
        else:
            line = line.strip()
            if not line.endswith(','):
                line += '|'
            line = '|  ' + line.replace('\n', '')
            line = line.replace('\t', '')
            line = line.replace(':', '  |  ')
            line = line.replace(',', '|')
            line += ' |\n'
            
            current_line = line

        new_content.append(current_line)
    return new_content

# 创建markdown格式的文档
def createMarkdownFile(filename, content_list):
    content  = filename + 's集合\n\r'
    content += """|字段|类型|注释|\n|:----    |:-------    |------      |\n"""
    print(content)
    for line in content_list:
        content += line

    file = open('./markdownfiles/' + filename + '.txt', 'w', encoding='utf-8')
    file.write(content)
    file.close()

# E:\emtwork\new-api\models\cms.jsmarkdownfiles
# 读取到文件内容
# file_path = "E:/emtwork/new-api/models/cms.js"
# model_file = open(file_path, 'r', encoding='utf-8')
# content = model_file.read()
# models\apointHandleGroup.js
ori_model_folder_path = 'E:/emtwork/new-api/models/'; 

ori_models = get_file_name_from_path(ori_model_folder_path)
#print(ori_models)
#exit(0)
#ori_models = ['companyApp.js','companyAnn.js','authority.js','cmsComment.js', 'cmsGroup.js', 'aweekActivity.js', 'appGroup.js', 'apointHandle.js', 'apointHandleGroup.js'];
ori_models2 = ['smartAppStep.js', 'smartAppStatement.js','smartAppDataRef.js','smartApp.js','interview.js','iflowShowtpl.js','hospital_privilleage.js','hospital.js','health_check.js','decisionMeeting.js','decisionIssue.js','decisionIssue_step.js','decisionExecute.js','decisionExecute_step.js', 'counter.js','counter_shift.js'];
ori_models = ['stl_weekplan.js', 'stl_customer.js', 'stl_timeline.js']
total = 0
for model in ori_models:
    full_path = ori_model_folder_path + model
    new_file_path = model
    print('prepare to create from ' + model + '\n')
    content_list = getSchemaPart(full_path, './' + new_file_path)
    if content_list == 0: 
        continue

    pure_model_without_ext = model.split('.')[0]
    print('without ext model is:' + pure_model_without_ext + '\n')
    createMarkdownFile(pure_model_without_ext, content_list)
    total += 1

print('total create file num is:' + str(total))
#str = '// xxxxx //xxxx'
#print(str.find('//'))
#model_file.close()