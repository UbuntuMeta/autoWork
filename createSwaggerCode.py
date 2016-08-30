# -*- coding: utf-8 -*-

'''
     Aim to using draft code to create complete swagger api-docs

     @version 0.1v
     @author freemannow <fightforphp@gmail.com>
'''


class SwaggerCode(object):

     def __init__(self, filepath):
          self.filepath = filepath
          self.outpath = './out.txt'
          self.content = []
          self.outContent = ''

     def getOriContent(self):
          with open(self.filepath, "r") as fh:
            content = fh.read()
            print(content)
            exit(0)
          # for line in fh.readlines():
          #    self.content.append(line.strip())
          # fh.close()
          # if (self.content == []):
          #    exit('没有需要生成的swagger代码！')

     def createCode(self):
          code = '''
     /**
     * @SWG\Get(
     *   path="
     
     ''' + self.content[0] +'''
     ",
     *   tags={"users"},
     *   summary="查询用户信息",
     *   description="",
     *   operationId="indexAction",
     *   produces={"application/json"},
     *   @SWG\Parameter(
     *     in="header",
     *     name="Authorization",
     *     description="access token",
     *     required=false,
     *     type="string",
     *   ),
     *   @SWG\Parameter(
     *     in="query",
     *     name="page",
     *     description="当前页数",
     *     required=false,
     *     default=1,
     *     type="integer",
     *     format="int32"
     *   ),
     *   @SWG\Parameter(
     *     in="query",
     *     name="limit",
     *     description="限制条数",
     *     required=false,
     *     default=20,
     *     type="integer",
     *     format="int32"
     *   ),
     *   @SWG\Response(
     *     response=200,
     *     description="user collection",
     *     @SWG\Schema(
     *       required={"total", "items"},
     *       @SWG\Property(
     *         property="total",
     *         type="integer",
     *         description="查询结果总数"
     *       ),
     *       @SWG\Property(
     *         property="items",
     *         type="array",
     *         @SWG\Items(ref="#/definitions/User")
     *       )
     *     )
     *   )
     * )
     */
                    '''
          
          self.outContent = code
     def saveToFile(self):
          out = open(self.outpath, 'w')
          out.write(self.outContent)
          out.close()

     def create(self):
          self.getOriContent()
          # print self.content
          self.createCode()
          self.saveToFile()
          # 


swagger = SwaggerCode('./draft.txt')
swagger.create()
