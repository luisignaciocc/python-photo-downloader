import datetime
import logging
import pymongo
import requests
from urllib.parse import quote
from tenacity import retry

class Process():

    def __init__(self, cfg):
        
        logfile='./log/download-{:%Y_%m_%d_%H_%M}.log'.format(datetime.datetime.now())
        logging.basicConfig(
            level=logging.INFO,
            filename=logfile,
            datefmt='%Y-%m-%d %H:%M:%S',
            format='%(asctime)s %(levelname)-8s %(message)s')
        self.logger = logging.getLogger('downloader')
        
        # self.client = pymongo.MongoClient('mongodb://{0}:{1}@{2}/{3}'.format(
        #     quote(cfg['auth'][cfg['env']]['mongo-user']),
        #     quote(cfg['auth'][cfg['env']]['mongo-pass']),
        #     cfg['auth'][cfg['env']]['mongo-host'],
        #     cfg['auth'][cfg['env']]['mongo-db'])
        # )

        # self.db = self.client[self.cfg['auth'][self.cfg['env']]['mongo-db']]

    @retry
    def _get_data(self, page):
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

        houses_data = self._get_data(1)
        for item in houses_data:
            print(item)

        self.logger.info(' ------------------')
        self.logger.info('| PROCESS FINISHED |')
        self.logger.info(' ------------------')


if __name__ == '__main__':
    Process().process()
