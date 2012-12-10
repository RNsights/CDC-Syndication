from bs4 import BeautifulSoup
import requests
import MySQLdb
import database_settings

# XML list of all  the topics availavle from the CDC syndication hub
cdc_topic_xml = 'http://t.cdc.gov/xml/lists/Topic.list'

r = requests.get(cdc_topic_xml)

soup = BeautifulSoup(r.text)

db = MySQLdb.connect(host=database_settings.DATABASE_HOST, user=database_settings.DATABASE_USER, passwd=database_settings.DATABASE_PASSWD, db=database_settings.DATABASE_DB)
cur = db.cursor()

topics = soup.find_all('vocabularyitem')

try:
	# Crate the CDC_Topics table if it doesn't already exist
	cur.execute("CREATE TABLE IF NOT EXISTS CDC_Topics ( Id int(11) NOT NULL DEFAULT '0', Topic varchar(255) DEFAULT NULL, Subscribe tinyint(1) DEFAULT '0', PRIMARY KEY (Id))")
except Exception, err:
	print err

for topic in topics:
	try:
		cur.execute("INSERT into CDC_Topics (Id, Topic) VALUES (%s, %s)", (topic['itemid'], topic['value'].encode('ascii', 'xmlcharrefreplace')))
		db.commit()
	except Exception, err:
		print err
		db.rollback()
		
print 'Done importing CDC Syndication Topics!'
		
cur.close()
db.commit()
db.close()

