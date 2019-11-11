import requests
import pyqrcode
from subprocess import call

url1= 'https://lnsms.world/invoice'
data1 = {'number':'+17203334371','text':'Lightning Programmable Texts! BIG',}
r = requests.post(url1,data=data1)
pr = r.text
url = pyqrcode.create(pr, error='L')
url.png("test.png",scale=6)
call(['xdg-open','test.png'])
# print(url.terminal(quiet_zone=1))