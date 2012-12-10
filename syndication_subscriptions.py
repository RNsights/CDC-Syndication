import feedparser
import MySQLdb
import database_settings

db = MySQLdb.connect(host=database_settings.DATABASE_HOST, user=database_settings.DATABASE_USER, passwd=database_settings.DATABASE_PASSWD, db=database_settings.DATABASE_DB)
cur = db.cursor()

# The number of days back to pull information from a given CDC Syndication feed.
days = "1000"

try:
	# create the CDC_Syndication_Items table if it doesn't already exist
	cur.execute("CREATE TABLE IF NOT EXISTS CDC_Syndication_Items (id int(11) unsigned NOT NULL AUTO_INCREMENT, itemid varchar(255) NOT NULL, topicid int(11) NOT NULL, title varchar(255) NOT NULL, creation_date datetime NOT NULL, modified_date datetime NOT NULL, url varchar(255) NOT NULL, PRIMARY KEY (id), UNIQUE KEY itemid (itemid)) ")
except Exception, err:
	print err

try:
	cur.execute("SELECT id, topic from CDC_Topics where subscribe = 1")
except Exception, err:
	print err
	
topics = cur.fetchall()

for topic in topics:
	items = feedparser.parse('http://t.cdc.gov/feed.aspx?tpc='+str(topic[0])+'&days='+days+'&src=1&fmt=ATOM')
	for entry in items.entries:
		try:
			cur.execute("INSERT into CDC_Syndication_Items (itemid, topicid, title, creation_date, modified_date, url) VALUES (%s, %s, %s, %s, %s, %s)", (entry.contentitem['guid'], topic[0], entry.title.encode('ascii', 'xmlcharrefreplace'), entry.catalogitem['addeddatetime'], entry.catalogitem['modifieddatetime'], entry.contentitem['persistenturl']))
			db.commit()
		except Exception, err:
			print err
			db.rollback()
			
print 'Done importing CDC Syndication subscriptions!'
		
cur.close()
db.commit()
db.close()

