import threading


def  loop():
    for i in range(50):
        print i,'\n'


for i in range(10):
    print 'start %s '%i
    threading.Thread(target=loop).start()