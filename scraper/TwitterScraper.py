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
path = parser.get('output_settings', 'outputPath')
class TwitterScraper(implements(iScraper)):
    tweets = None

    def scrape(self, topic, language):
        c = twint.Config()
        c.Lang = language
        c.Store_csv = True
        c.Custom["tweet"] = ["tweet", "date", "username", "hashtags", "link"]
        c.Output = path+"tweets-" + topic + "-" + str(date.today()) + ".csv"
        if parser.get('scraper_settings', 'strictMode').lower() == 'true':
            c.Search = ["Škoda", topic]
        else:
            c.Search = [topic]
        if exists(path+"tweets-" + topic + "-" + str(date.today()) + ".csv"):
            return print("Tweets for " + topic + "was already scraped for today.")
        else:
            print("Scraping Twitter Data For Keyword " + topic + "...")
            self.tweets = twint.run.Search(c)

            file = open(path+"tweets-" + topic + "-" + str(date.today()) + ".csv")
            csvReader = csv.reader(file)
            header = next(csvReader)
            header.append("lang")
            rows = []
            for row in csvReader:
                rows.append(row)
                row.append(detect(row[0]))
            with open(path + "tweets-" + topic + "-" + str(date.today()) + ".csv", 'w', encoding='UTF8') as file:
                writer = csv.writer(file)
                writer.writerow(header)
                writer.writerows(rows)
    def getData(self):
        if not self.tweets == None:
            return self.tweets
        else:
            return "No Tweets Found"

    def printTweetWordsToCSV(self):
        langs = dict()
        for topic in parser.get('scraper_settings', 'keywords').split(','):
            file = open(path + "tweets-" + topic.strip() + "-" + str(date.today()) + ".csv")
            csvReader = csv.reader(file)
            header = next(csvReader)
            rows = []
            for row in csvReader:
                rows.append(row)
                if not row[len(row) - 1] in langs:
                    print("Adding language " + row[len(row) - 1] + " to langs dictionary...")
                    langs[row[len(row) - 1]] = Counter()

                for word in row[0].split():
                    langs[row[len(row) - 1]][word] += 1
            file.close()
        with open(path + 'tweet-'+ str(date.today()) + '-words.csv', 'w', encoding='UTF8') as file:
            writer = csv.writer(file)
            writer.writerow(["lang", "word", "count"])
            for lang in langs:
                for word in langs[lang].most_common(int(parser.get('output_settings', 'topWords'))):
                    writer.writerow([lang, word[0], word[1]])
        print(langs)