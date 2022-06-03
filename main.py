from scraper.TwitterScraper import TwitterScraper
from configparser import ConfigParser

parser = ConfigParser()
parser.read('config.ini')

for topic in parser.get('scraper_settings', 'keywords').split(','):
        scraper = TwitterScraper()
        scraper.scrape(topic.strip())
        tweets = scraper.getData()
        print(tweets)

if parser.get('output_settings', 'enableWordsOutput').lower() == "true":
        scraper.printTweetWordsToCSV()

if parser.get('output_settings', 'enableCountOutput').lower() == "true":
        scraper.printTweetCountsToCSV()