from scraper.TwitterScraper import TwitterScraper
from configparser import ConfigParser

parser = ConfigParser()
parser.read('config.ini')

for topic in parser.get('scraper_settings', 'keywords').split(','):
    #for language in parser.get('scraper_settings', 'languages').split(','):
        language = 'en'
        scraper = TwitterScraper()
        scraper.scrape(topic.strip(), language)
        tweets = scraper.getData()
        print(tweets)
scraper.printTweetWordsToCSV()