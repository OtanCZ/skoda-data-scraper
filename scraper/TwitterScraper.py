from interface import implements
from scraper.iscraper import iScraper
from configparser import ConfigParser
from datetime import date
from os.path import exists
from collections import Counter
from langdetect import detect
import twint
import csv

parser = ConfigParser()
parser.read('config.ini')

class TwitterScraper(implements(iScraper)):
    tweets = None

    def scrape(self, topic, language):
        c = twint.Config()
        c.Lang = language
        c.Store_csv = True
        c.Custom["tweet"] = ["tweet", "date", "username", "hashtags", "link"]
        c.Output = "tweets-" + topic + "-" + str(date.today()) + ".csv"
        if parser.get('scraper_settings', 'strictMode').lower() == 'true':
            c.Search = ["Škoda", topic]
        else:
            c.Search = [topic]
        if exists("./tweets-" + topic + "-" + str(date.today()) + ".csv"):
            return print("Tweets for " + topic + "was already scraped for today.")
        else:
            print("Scraping Twitter Data For Keyword " + topic + "...")
            self.tweets = twint.run.Search(c)

            file = open("./tweets-" + topic + "-" + str(date.today()) + ".csv")
            csvReader = csv.reader(file)
            header = next(csvReader)
            header.append("lang")
            rows = []
            langs = dict()
            for row in csvReader:
                rows.append(row)
                row.append(detect(row[0]))
                # for every word in row put in counter
                ##print(row)
                # add Counter to idklol if language is not present from last row
                if not row[len(row)-1] in langs:
                    print("Adding language " + row[len(row)-1] + " to idklol")
                    langs[row[len(row)-1]] = Counter()

                for word in row[0].split():
                    langs[row[len(row)-1]][word] += 1

            print(langs)

    def getData(self):
        if not self.tweets == None:
            return self.tweets
        else:
            return "No Tweets Found"

    def printToCSV(self):
        pass