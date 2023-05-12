import requests
import time
from PIL import Image
import io
import os
from multiprocessing import Queue
from threading import Thread
from pathlib import Path


class ImageDownloader:
    def __init__(self, image_queue, save_path):
        self.image_queue = image_queue
        self.save_path = save_path
        self.listener = Thread(target=self.queue_listener)

        if not os.path.exists(self.save_path):
            print(f"{self.save_path} does not exist")
            os.makedirs(self.save_path)
            print(f"Created path: {self.save_path}")


    def queue_listener(self):
        while True:
                item = self.image_queue.get()

                if item is None:
                    time.sleep(0.1)
                    break
                
                (index, img_url) = item
                Thread(target=self.download_img, args=(img_url, f"{self.save_path}/{index}.jpg")).run()

    def start_listener(self):
        self.listener.start()

    def stop_listener(self):
        self.listener.join()

    def download_img(self, img_url, save_path):
        try:
            image = requests.get(img_url).content
            image = Image.open(io.BytesIO(image))
            image = image.convert('RGB')
            image.save(save_path)
        except:
            print(f"[ERROR]: {img_url}")

