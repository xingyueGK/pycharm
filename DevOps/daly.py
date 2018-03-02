import  threading
import  requests
import os

def  gets():
    print 'fsf'
    url = 'http://10.163.145.189:8088/beefly-diqin-admin-web-1.0.0-SNAPSHOT/init/listPageBattery?token=747aa32860c8452693e313b75c410a67'
    text = requests.get(url)

    print text.text()

gets()

# while True:
#     threading.Thread(target=gets).start()