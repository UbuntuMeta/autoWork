import os
os.system("ls");

# 检查emt仓库的该项目是否存在
emtwork = '/e/emtwork'
workplace = 'e:/emtwork'
project_name = 'tsb-passport'
branch = 'master'

# if os.path.exists(emtwork + '/' + project_name):
#     print('have the folder!\r\n')

# else:
#     #print('not have the folder!')
#     cmd = '''
#     git clone emt-git:%s && mv %s %s/%s
#     ''' %(project_name, project_name, emtwork, project_name)
#     print(cmd)
#     exit(100)
#     os.system(cmd)


def getProject(emtwork, project_name):
    full_path = workplace + '/' + project_name
    print(full_path)
    if os.path.exists(full_path):
        print('have the folder!\r\n')
        return;
    else:
        print('not have the folder!')
        cmd = '''
        git clone emt-git:%s && mv %s %s/%s
        ''' %(project_name, project_name, emtwork, project_name)
        print(cmd)
        os.system(cmd)
        return;

getProject(emtwork, project_name)
