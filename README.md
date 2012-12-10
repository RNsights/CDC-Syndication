CDC-Syndication
===============

A couple of basic scripts to pull and store content from the CDC Syndication Hub (http://tools.cdc.gov/syndication/) using Python and MySQL.

### Generate a Table of Syndication Topics

The first script, syndication_topics.py, uses the Requests module (http://docs.python-requests.org/) to request the XML list of all syndication topics via an HTTP GET request and uses BeautifulSoup (http://www.crummy.com/software/BeautifulSoup/) to parse out the individual topic information, specifically topic title and id.

Both packages can be installed using pip:

    $ pip install requests

and

    $ pip install beautifulsoup4

Before running this script, make sure to update the database_settings.py with your MySQL connection information.

When you run this script it will create a table, CDC_Topics, with the id, topic title and a subscribe field set to 0. You'll need to set this field to 1 for each topic you want to subscribe to. Topic ids are unique, so if you run this script multiple times, the database will prevent you from adding duplicate topics to the table.

### Generate a Table of Syndication Items and Pull Subscriptions

The second script, syndication_subscriptions.py, uses the feedparser module (http://code.google.com/p/feedparser/) to parse the atom feeds available from the CDC Syndication Hub. Feedparser can also easily be installed using pip.

    $ pip install feedparser

Once you've set up some subscriptions in the CDC_Topics table, run this script to create the CDC_Syndication_Items table and pull any content available from the selected feeds. By default, the request to the atom feed for each topic goes back 1000 days. This is set by the days variable on line 9:

    days = "1000"

Just like the CDC_Topics table, the CDC_Syndication_Items table has a unique index on the itemid field (this the guid from the atom feed). If you run this script multiple times, the unqiue contraint will prevent duplicate items from being added to the database.

And that's it. I'd suggest just setting up a cron job or the like to run the syndication_subscriptions.py script on a periodic basis. You should now have two tables filled with the data needed to collect, sort, aggregate and display content from the CDC Syndication Hub.