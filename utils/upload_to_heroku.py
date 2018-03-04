import os
import requests
#from bs4 import BeautifulSoup

path = '/home/andrey_g/mro/schneider/pdf'
files = os.listdir(path)

files_app = []
i = 0
for file in files:
    # os.rename(os.path.join(path, file), os.path.join(path, 'gates_igs_' + os.path.splitext(os.path.basename(file))[0] +'.igs'))
    # files = {'file1': open('report.xls', 'rb'), 'file2': open('otherthing.txt', 'rb')}
    # files={'file_field': open(os.path.join(path, file), 'rb')}
    # files = [('file_field': open(os.path.join(path, file), 'rb'))]
    # if file == 'gates_igs_7_A90.igs':
    #     print i
    '''
    if i > 1317:
        continue
    '''
    i += 1
    file_ex = {'file_field': open(os.path.join(path, file), 'rb')}
    s = requests.Session()
    # soup = BeautifulSoup(c.content)
    # csrf = soup.find("input", type="hidden", value=True)["value"]
    r = s.post(
            'https://mro-host.herokuapp.com/',
            headers={
                'referer': 'https://mro-host.herokuapp.com/',
                'User-Agent': 'Mozilla/5.0'
            },
            files=file_ex
    )
    print i
    print file
    # https://mro-host.herokuapp.com/
