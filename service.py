import gevent.monkey; gevent.monkey.patch_all()
from model import Listing
import bottle
import httplib
import logging
import os
import csv
import urllib2
from geojson import Feature, Point, FeatureCollection

app = bottle.Bottle()
listings = []
log = logging.getLogger(__name__)

def load_listings(csv_url):
    listings = []
    content = urllib2.urlopen(csv_url)
    cr = csv.reader(content)
    for row in cr:
        listing_id, street, status, price, bedrooms, bathrooms, sq_ft, longitude, latitude = row
        if listing_id == 'id':
            continue  # skip the first row (header)

        price = float(price)
        sq_ft = float(sq_ft)
        bathrooms = int(bathrooms)
        longitude = float(longitude)
        latitude = float(latitude)


        listing = Listing(
            listing_id, street, status, price,
            bedrooms, bathrooms, sq_ft, longitude, latitude
        )
        listings.append(listing)
    return listings


@app.get('/health')
def health_check():
    """
    Health check endpoint
    """
    return {'OK': 1}


def to_geojson(listings):
    features = []
    for listing in listings:
        point = Point((listing.longitude, listing.latitude))
        features.append(Feature(geometry=point, properties = {'id': listing.id, 'price': listing.price, 'street': listing.street, 'bedrooms': listing.bedrooms, 'bathrooms': listing.bathrooms, 'sq_ft': listing.sq_ft}))
    feature_collection = FeatureCollection(features)
    return feature_collection

@app.get('/listings')
def listings():
    """
    Get the listings
    """
    return to_geojson(listings)

if __name__ == '__main__':
    # load the csv file into the listing model
    listings = load_listings('https://s3.amazonaws.com/opendoor-problems/listings.csv')
    app.run(
        host='0.0.0.0',
        port=os.environ.get('PORT', 5000),
        server='gevent'
    )
