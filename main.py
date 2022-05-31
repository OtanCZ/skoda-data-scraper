from scraper.TwitterScraper import TwitterScraper
from configparser import ConfigParser

parser = ConfigParser()
parser.read('config.ini')

for topic in parser.get('scraper_settings', 'keywords').strip().split(','):
    for language in parser.get('scraper_settings', 'languages').strip().split(','):
        scraper = TwitterScraper()
        scraper.scrape(topic, language)
        tweets = scraper.getData()
        print(tweets)