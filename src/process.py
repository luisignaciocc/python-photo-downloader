import datetime
import logging
import pymongo
import requests
from os import path
from urllib.parse import quote
from tenacity import retry, stop_after_attempt, stop_after_delay

class Process():

    def __init__(self, cfg, photos_dir):
        self.page_limit = 10

        logfile='./log/download-{:%Y_%m_%d_%H_%M}.log'.format(datetime.datetime.now())
        logging.basicConfig(
            level=logging.INFO,
            filename=logfile,
            datefmt='%Y-%m-%d %H:%M:%S',
            format='%(asctime)s %(levelname)-8s %(message)s')
        self.logger = logging.getLogger('downloader')
        
        self.client = pymongo.MongoClient('mongodb://{0}:{1}@{2}/{3}'.format(
            quote(cfg['auth'][cfg['env']]['mongo-user']),
            quote(cfg['auth'][cfg['env']]['mongo-pass']),
            cfg['auth'][cfg['env']]['mongo-host'],
            cfg['auth'][cfg['env']]['mongo-db'])
        )

        self.db = self.client[cfg['auth'][cfg['env']]['mongo-db']]
        self.db.houses.create_index([('id',  pymongo.ASCENDING)], name='unique-id', default_language='english',unique=True)

        self.photos_dir = photos_dir

    @retry(stop=stop_after_delay(10))
    def _download_image(self, house):
        image_id = house["id"]
        image_addr = house["address"].replace(" ", "_").replace(".", "").replace(",", "")
        image_ext = house["photoURL"].rpartition(".")[-1]
        image_name = f'id-{image_id}-{image_addr}.{image_ext}'
        photo_path = path.join(self.photos_dir, image_name)
        response = requests.get(house["photoURL"])
        file = open(photo_path, "wb")
        file.write(response.content)
        file.close()
        return image_name

    @retry(stop=stop_after_attempt(10))
    def _get_data(self, page):
        self.logger.info(f'Downloading page {page} of {self.page_limit}')
        return requests.get('http://app-homevision-staging.herokuapp.com/api_project/houses', 
            headers={
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Accept-Language': 'en-US,en;q=0.9,es;q=0.8',
            }, 
            params=(
                ('page', page),
            ),
            verify=False).json()['houses']


    def process(self):
        self.logger.info(' -----------------')
        self.logger.info('| PROCESS STARTED |')
        self.logger.info(' -----------------')

        page = 0
        while page < self.page_limit:
            page += 1
            try:
                houses_data = self._get_data(page)
            except:
                self.logger.error(f'Error downloading page {page}, skipping')
                pass
            for item in houses_data:
                if self.db.houses.count_documents({'id':  item['id'] }) == 0:
                    try:
                        image_name = self._download_image(item)
                    except:
                        image_name = 'not_downloaded'
                    item['image_name'] = image_name
                    self.db.houses.insert_one(item)

        self.logger.info(' ------------------')
        self.logger.info('| PROCESS FINISHED |')
        self.logger.info(' ------------------')


if __name__ == '__main__':
    Process().process()
