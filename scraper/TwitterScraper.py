from interface import implements
from scraper.iscraper import iScraper
from configparser import ConfigParser
import twint

parser = ConfigParser()
parser.read('config.ini')

class TwitterScraper(implements(iScraper)):
    tweets = None

    def scrape(self, topic, language):
        print("Scraping Twitter Data For Keyword " + topic + " in " + language)
        c = twint.Config()
        c.Lang = language
        if parser.get('scraper_settings', 'strictMode').lower() == 'true':
            c.Search = ["Škoda", topic]
        else:
            c.Search = [topic]
        self.tweets = twint.run.Search(c)

    def getData(self):
        return self.tweets

