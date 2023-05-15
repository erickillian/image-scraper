from imagescraper import ImageScraperDriver
from downloader import ImageDownloader
from multiprocessing import Queue
import time
import requests
import json

url = 'https://datasets-server.huggingface.co/first-rows?dataset=Drozdik%2Ftattoo_v3&config=Drozdik--tattoo_v3&split=train'

image_queue = Queue(maxsize=50)
image_downloader = ImageDownloader(
    image_queue = image_queue, 
    save_path='./tattoos'
)

image_downloader.start_listener()

data_json = requests.get(url)
data = json.loads(data_json.text)

index = 0
for image in data['rows']:
    print("This happened")
    image_src = image['row']['image']['src']
    image_queue.put((index, image_src), block=True)
    index += 1



image_queue = Queue(maxsize=10)


image_downloader.stop_listener()
