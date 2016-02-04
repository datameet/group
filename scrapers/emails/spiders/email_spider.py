import scrapy
import urllib
import dataset
from bs4 import BeautifulSoup
from datetime import datetime

db = dataset.connect('sqlite:////media/thej/data2/group/group.sqlite')
db.begin()
db_topics_table = db['topics']
db_emails_table = db['emails']

urls = []
for topic in db_topics_table:
	urls.append("https://groups.google.com/forum/"+topic['topic_url'])

print str(urls)
	
class EmailSpider(scrapy.Spider):
    name = "emails"
    allowed_domains = ["groups.google.com"]
    start_urls = urls #['https://groups.google.com/forum/#!topic/datameet/V-a4yjeGhGM']
	
	
    def parse(self, response):
		soup = BeautifulSoup(response.body, 'html.parser')
		#from scrapy.shell import inspect_response
		#inspect_response(response, self)
		seq = 0
		topic = urllib.unquote(response.url).decode('utf8')
		topic = (topic.split("="))[-1]
		topic = "#"+topic 
		for row in soup.find_all('tr'):
			seq = seq + 1
			insert_data = {}
			td = row.find_all("td")
			insert_data["seq"] 			= str(seq)
			insert_data["subject"]		= (td[0]).get_text()
			insert_data["author"] 		= (td[1]).get_text()
			date_object = datetime.strptime(str((td[2]).get_text()), '%d/%m/%y %H:%M')
			insert_data["lastPostDate"] = date_object
			insert_data["snippet"] 		= (td[3]).get_text()
			insert_data["topic"] 		= topic
			print str(insert_data)
			db_emails_table.insert(insert_data)
			db.commit()
			
		
		