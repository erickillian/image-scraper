from imagescraper import ImageScraperDriver
from downloader import ImageDownloader
from multiprocessing import Queue
import time

query = "bananas"

save_folder = "./bananas"

url_blacklist = [
    'alamy',
    'shutterstock',
]

image_queue = Queue(maxsize=10)

google_scraper = ImageScraperDriver(
    images_xpath="//img[contains(@class,'rg_i')]", 
    selected_image_xpath="//img[contains(@class,'r48jcc') and contains(@class,'pT0Scc') and contains(@class,'iPVvYb')]",
    show_more_xpaths= ["//input[@type='button' and @value='Show more results' and not(@hidden)]", "//span[contains(@class,'r0zKGf') and contains(text(),'See more anyway')]", "//div[text()=\"Looks like you've reached the end\"]", "//a[class='frGj1b']"],   #Looks like you've reached the end
    search_url=f"https://www.google.com/search?q={query}&tbm=isch&tbs=isz:l",   #%2Cil:cl
    num_images=500, 
    image_queue=image_queue,
    url_blacklist=url_blacklist,
    # start_at=48
)

image_downloader = ImageDownloader(
    image_queue = image_queue, 
    save_path=save_folder,
)

image_downloader.start_listener()

google_scraper.run()

# Sleeps for 5 seconds so that all remaining images in the queue can finish downloading
time.sleep(5)

image_downloader.stop_listener()
