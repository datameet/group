import urllib3
urllib3.disable_warnings()
import math
import time
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import dataset

#*********************PLEASE UPDATE THIS***********************
base_url = 'https://groups.google.com/forum/'
base_group_url = base_url  + '#!forum/datameet'
base_topic_url = base_url  + '#!topic/datameet/'
#*********************PLEASE UPDATE THIS***********************


db = dataset.connect('sqlite:///../group.sqlite')
db.begin()
db_topics_table = db['topics']

with open ("./raw/topics.html", "r") as myfile:
   topics_html=myfile.read()
	
soup = BeautifulSoup(topics_html, 'html.parser')	

j = 0
for row in soup.find_all('tr'):
	j = j + 1
	print str("Row no =")+str(j)
	insert_dict = {}
	div_containers = row.contents[1]
	all_divs = div_containers.contents[0].contents[0].contents[0].contents[0].find_all("div")
	i = 0
	for div in all_divs:
		i = i + 1
		if i  == 2:
			try:
				insert_dict['username'] = str(div['aria-label']).replace("'s profile photo","")
				insert_dict['userid'] = str(div['data-userid'])
			except:
				pass
		if i ==5:
			try:
				ahref = div.find("a")
				insert_dict['topic_url'] = str(ahref['href'])
				insert_dict['topic'] = str(ahref.get_text())
			except:
				pass
			spans = div.find_all("span")

			try:	
				insert_dict['posts'] = str(spans[3].get_text()).replace(" posts","").replace(" post","")
				insert_dict['views'] = str(spans[4].get_text()).replace(" views","").replace(" view","")
			except:
				pass
			try:	
				time_span = spans[5].find("span")
				date_object = datetime.strptime(str((time_span["title"])), '%A, %d %B %Y %H:%M:%S UTC+5:30')
				insert_dict['date_time'] = date_object
			except:
				pass
	print str(insert_dict)
	db_topics_table.insert(insert_dict)
	db.commit()

