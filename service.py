import gevent.monkey; gevent.monkey.patch_all()
from opendoor.model import Listing
import bottle
import httplib
import logging
import os
import csv
import urllib2

app = bottle.Bottle()

log = logging.getLogger(__name__)

def load_listings(csv_url):
    listings = []
    content = urllib2.urlopen(csv_url)
    cr = csv.reader(content)

    for row in cr:
        logging.info(row)


@app.get('/health')
def health_check():
    """
    Health check endpoint
    """
    return {'OK': 1}

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=os.environ.get('PORT', 5000),
        server='gevent'
    )

    # load the csv file into the listing model
    listings = load_listings('https://s3.amazonaws.com/opendoor-problems/listings.csv')
