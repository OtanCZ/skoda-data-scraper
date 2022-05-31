from scraper.TwitterScraper import TwitterScraper
topics = ["Fabia", "Enyaq", "SuperB"]

for topic in topics:
    TwitterScraper.scrape(TwitterScraper, topic)
    print(TwitterScraper.getData(TwitterScraper))