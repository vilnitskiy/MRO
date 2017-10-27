import urllib
import urllib2
import shutil

req = urllib2.Request('http://www.skf.com/cadDownload/02017070816460853637162192d056f/PARTserver02017070816460853637162192d056f.zip')
resp = urllib2.urlopen(req)

with open('file.zip', 'wb') as file:
    shutil.copyfileobj(resp.fp, file)

