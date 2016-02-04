from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())

# 'emails' is the name of one of the spiders.
process.crawl('emails')
process.start() # the script will block here until the crawling is finished