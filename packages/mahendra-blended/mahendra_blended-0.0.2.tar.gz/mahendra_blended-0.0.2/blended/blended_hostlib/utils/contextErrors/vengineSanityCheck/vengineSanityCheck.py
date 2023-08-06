import os
cur_dir = os.path.dirname(os.path.abspath(__file__))
sanityCheckFilePath = os.path.join( cur_dir, 'sanityCheck.js')
file = open(sanityCheckFilePath, 'r',encoding='utf8')
sanityCheckFile = {'content': file.read()}
