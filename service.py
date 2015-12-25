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


def filter_listings(listings, min_bedrooms, max_bedrooms, min_bathrooms, max_bathrooms, min_price, max_price):
    filtered_listings = []
    if not listings:
        # returning here because it could be None in addition to being a []
        return filtered_listings
    for listing in listings:
        if min_bedrooms and listing.bedrooms < min_bedrooms:
            continue
        if max_bedrooms and listing.bedrooms > max_bedrooms:
            continue
        if min_bathrooms and listing.bathrooms < min_bathrooms:
            continue
        if max_bathrooms and listing.bathrooms > max_bathrooms:
            continue
        if min_price and listings.price < min_price:
            continue
        if max_price and listings.price < max_price:
            continue
        filtered_listings.append(listing)
    return filtered_listings


@app.get('/listings')
def listings():
    """
    Get the listings
    """

    # get the filter params
    min_bedrooms = bottle.request.GET.get('min_bed')
    max_bedrooms = bottle.request.GET.get('max_bed')

    min_bathrooms = bottle.request.GET.get('min_bath')
    max_bathrooms = bottle.request.GET.get('max_bath')

    min_price = bottle.request.GET.get('min_price')
    max_price = bottle.request.GET.get('max_price')

    min_bedrooms = int(min_bedrooms) if min_bedrooms else None
    max_bedrooms = int(max_bedrooms) if max_bedrooms else None

    min_bathrooms = int(min_bathrooms) if min_bathrooms else None
    max_bathrooms = int(max_bathrooms) if max_bathrooms else None

    min_price = float(min_price) if min_price else None
    max_price = float(max_price) if max_price else None

    listings = filter_listings(listings, min_bedrooms, max_bedrooms, min_bathrooms, max_bathrooms, min_price, max_price)
    return to_geojson(listings)

if __name__ == '__main__':
    # load the csv file into the listing model
    listings = load_listings('http://s3.amazonaws.com/opendoor-problems/listings.csv')
    app.run(
        host='0.0.0.0',
        port=os.environ.get('PORT', 5000),
        server='gevent'
    )
