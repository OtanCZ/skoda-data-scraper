from interface import implements
from scraper.iscraper import iScraper
import twint


class TwitterScraper(implements(iScraper)):
    tweets = None

    def scrape(self, topic):
        print("Scraping Twitter Data For Keyword " + topic)
        c = twint.Config()
        c.Search = ["Škoda", topic]
        self.tweets = twint.run.Search(c)

    def getData(self):
        return self.tweets

