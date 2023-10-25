import threading
import time
import logging
import random
from multiprocessing import Queue

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)

BUF_SIZE = 10
q = Queue(maxsize=BUF_SIZE)

class UrlScraperThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(UrlScraperThread,self).__init__()
        self.target = target
        self.name = name
        self.q = args[0]

    def run(self):
        while True:
            item = random.randint(1,10)
            q.put(item, block=True)
            time.sleep(0.1)
        return

class DownloaderThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(DownloaderThread,self).__init__()
        self.target = target
        self.name = name
        return

    def run(self):
        while True:
            if not q.empty():
                item = q.get()
                logging.debug('Getting ' + str(item) 
                              + ' : ' + str(q.qsize()) + ' items in queue')
            time.sleep(0.05)
        return

if __name__ == '__main__':
    
    p = UrlScraperThread(name='producer')
    c = DownloaderThread(name='consumer')

    p.start()
    time.sleep(2)
    c.start()
    time.sleep(2)