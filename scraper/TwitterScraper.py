import os
from interface import implements
from scraper.iscraper import iScraper
from configparser import ConfigParser
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
    usedDates = []

    def scrape(self, topic):
        if exists(path + 'tweets-' + topic + '.csv'):
            print("File already exists, removing...")
            os.remove(path + 'tweets-' + topic + '.csv')

        c = twint.Config()
        c.Store_csv = True
        c.Custom["tweet"] = ["tweet", "date", "username", "hashtags", "link"]
        c.Output = path + "tweets-" + topic + ".csv"
        if parser.get('scraper_settings', 'strictMode').lower() == "true":
            c.Search = [parser.get('scraper_settings', 'strictWord'), topic]
        else:
            c.Search = [topic]

        print("Scraping Twitter Data For Keyword " + topic + "...")
        self.tweets = twint.run.Search(c)

        file = open(path + "tweets-" + topic + ".csv")
        csvReader = csv.reader(file)
        header = next(csvReader)
        header.append("lang")
        rows = []
        for row in csvReader:
            rows.append(row)
            try:
                row.append(detect(row[0]))
            except:
                row.append("N/A")

        with open(path + "tweets-" + topic + ".csv", 'w', encoding='UTF8') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(rows)
    def getData(self):
        if not self.tweets == None:
            return self.tweets
        else:
            return "No Tweets Found"

    def isInUsedDates(self, date):
        if not date in self.usedDates:
            self.usedDates.append(date)
            return False
        else:
            return True

    def printTweetCountsToCSV(self):
        with open(path + 'tweet-counts.csv', 'w', encoding='UTF8') as mfile:
            writer = csv.writer(mfile)
            writer.writerow(["date", "lang", "keyword", "count"])
            tweetCount = dict()

            for topic in parser.get('scraper_settings', 'keywords').split(','):
                file = open(path + 'tweets-' + topic.strip() + '.csv')
                csvReader = csv.reader(file)
                header = next(csvReader)
                for row in csvReader:
                    if not (topic.strip() + "." + row[1] + "." + row[len(row)-1]) in tweetCount:
                        tweetCount[topic.strip() + "." + row[1] + "." + row[len(row)-1]] = 1
                    else:
                        tweetCount[topic.strip() + "." + row[1] + "." + row[len(row)-1]] += 1

            for count in tweetCount:
                writer.writerow([count.split(".")[1], count.split(".")[2], count.split(".")[0], tweetCount[count]])

    def printTweetWordsToCSV(self):
        with open(path + 'tweet-words.csv', 'w', encoding='UTF8') as mfile:
            writer = csv.writer(mfile)
            writer.writerow(["date", "lang", "keyword", "word", "count"])

            for topic in parser.get('scraper_settings', 'keywords').split(','):
                file = open(path + 'tweets-' + topic.strip() + '.csv')
                self.usedDates = []
                csvReader = csv.reader(file)
                header = next(csvReader)
                allrows = []
                sortedrows = []
                print(topic)
                langdates = dict()
                for row in csvReader:
                    allrows.append(row)

                for sortedrow in allrows:
                    if not self.isInUsedDates(sortedrow[1]):
                        temp_row = []
                        for row1 in allrows:
                            if sortedrow[1] == row1[1]:
                                temp_row.append(row1)
                        for row5 in temp_row:
                            for word in row5[0].split():
                                if len(word) > int(parser.get('output_settings', 'minWordSize')):
                                    if not row5[len(row5) - 1] in langdates:
                                        print("Adding language " + row5[len(row5) - 1] + " to langs dictionary...")
                                        langdates[row5[len(row5) - 1]] = Counter()
                                    else:
                                        langdates[row5[len(row5) - 1]][word] += 1
                        for lang in langdates:
                            for word in langdates[lang].most_common(int(parser.get('output_settings', 'topWords'))):
                                sortedrows.append([temp_row[0][1], lang, topic ,word[0], word[1]])
                    else:
                        continue

                writer.writerows(sortedrows)