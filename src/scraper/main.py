import argparse
import toml
from scraper.imagescraper import ImageScraperDriver
from scraper.downloader import ImageDownloader
from multiprocessing import Queue
import time
import os
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR)
CONFIG_DIR = os.path.join(PARENT_DIR, 'configs')

def urlify(s):

    # Remove all non-word characters (everything except numbers and letters)
    s = re.sub(r"[^\w\s]", '', s)

    # Replace all runs of whitespace with a single dash
    s = re.sub(r"\s+", '-', s)

    return s

def start(query, save_folder, num_images, blacklist, headless, scraper_config):
    url_blacklist = blacklist.split(",") if blacklist else []
    image_queue = Queue(maxsize=10)

    scraper = ImageScraperDriver(
        images_xpath=scraper_config['images_xpath'],
        selected_image_xpath=scraper_config['selected_image_xpath'],
        show_more_xpaths=scraper_config['show_more_xpaths'],
        search_url=scraper_config['base_search_url'].format(query=query),
        num_images=num_images,
        image_queue=image_queue,
        headless=headless,
        url_blacklist=url_blacklist,
    )

    image_downloader = ImageDownloader(
        image_queue=image_queue,
        save_path=save_folder,
    )

    image_downloader.start_listener()
    scraper.run()
    time.sleep(10)
    image_downloader.stop_listener()

def get_configs():
    """
    Get all configurations from TOML files.
    """
    config_files = [f for f in os.listdir(CONFIG_DIR) if os.path.isfile(os.path.join(CONFIG_DIR, f)) and f.endswith('.toml')]
    
    all_configs = {}
    for file in config_files:
        file_path = os.path.join(CONFIG_DIR, file)
        configs = toml.load(file_path)
        for key, value in configs.items():
            all_configs[key] = value
        
    return all_configs

def main():
    parser = argparse.ArgumentParser(description="Image Scraper Script")
    parser.add_argument("--query", help="Search query for images")
    parser.add_argument("--save_folder", help="Directory to save downloaded images")
    parser.add_argument("--num_images", type=int, default=500, help="Number of images to scrape")
    parser.add_argument("--blacklist", default="alamy,shutterstock", help="Comma-separated list of domains to blacklist")
    
    parser.add_argument("--config", default="GoogleImagesLarge", help="Specify a configuration file or title within the 'configs' directory")
    
    parser.add_argument("--list-configs", action='store_true', help="List available TOML configuration files in the 'configs' directory")
    parser.add_argument("--headless", action='store_true', default=True, help="Run in headless mode")

    args = parser.parse_args()

    config_mapping = get_configs()

    if args.save_folder is None:
        args.save_folder = args.query

    config_key=None
    
    if args.list_configs:
        print("Available Image Scraper Configs:")
        for title in config_mapping.keys():
            print(f"- {title}")
    else:
        if args.config in config_mapping:
            configs = config_mapping[args.config]
            config_key = str(args.config)
        elif args.config in list(config_mapping.keys()):
            configs = args.config
        else:
            print(config_mapping)
            print(list(config_mapping.keys()))
            print(f"Config '{args.config}' not found. Exiting.")
            return
        
        if config_key is None:
            config_key = list(configs.keys())[0]
        config = config_mapping[config_key]
        
        start(args.query, args.save_folder, args.num_images, args.blacklist, args.headless, config)

if __name__ == "__main__":
    main()