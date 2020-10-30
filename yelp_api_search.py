import csv
import decimal
import pprint
import requests
from urllib.parse import quote

API_KEY= 'API_KEY'

API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'

def request(host, path, api_key, url_params=None):
    """Given your API_KEY, send a GET request to the API.

    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        API_KEY (str): Your API Key.
        url_params (dict): An optional set of query parameters in the request.

    Returns:
        dict: The JSON response from the request.

    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }

    print(u'Querying {0} ...'.format(url))

    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()


def search(api_key, term, location, limit, offset):
    """Query the Search API by a search term and location.

    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.

    Returns:
        dict: The JSON response from the request.
    """

    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': limit,
        'offset': offset
    }
    return request(API_HOST, SEARCH_PATH, api_key, url_params=url_params)

if __name__ == '__main__':
    file = open("restaurant_info.csv", "a")
    writer = csv.writer(file)
    # writer.writerow(
    #     ['restaurant_id', 'restaurant_name', 'cuisine_type', 'restaurant_address', 'latitude',
    #      'longitude', 'manhattan_region', 'restaurant_rating', 'review_count', 'price'])

    cuisine_list = ['American', 'French', 'Italian', 'Mexican', 'Thai', 'Indian', 'Chinese', 'Japanese','Vietnamese', 'Caribbean', 'African', 'Greek', 'Korean', 'British', 'German']
    # cuisine_list = ['German']
    location = 'Manhattan, New York'

    for cuisine in cuisine_list:
        for offset in range(0, 999, 50):
            res = search(API_KEY, term=cuisine, location=location, limit=50, offset=offset)['businesses']
            for r in res:
                if r['location']['city'] == 'New York':
                    restaurant_id = r['id']
                    restaurant_name = r['name']
                    cuisine_type = cuisine
                    restaurant_address = "'"+(", ").join(r['location']['display_address'])+"'"
                    latitude = decimal.Decimal(str(r['coordinates']['latitude']))
                    longitude = decimal.Decimal(str(r['coordinates']['longitude']))
                    restaurant_rating = decimal.Decimal(str(r['rating']))
                    review_count = r['review_count']
                    price = r.get('price', None)
                    if latitude <= 40.734:
                        manhattan_region = 'Downtown'
                    elif 40.734 < latitude <= 40.766:
                        manhattan_region = 'Midtown'
                    elif 40.766 < latitude < 40.810:
                        manhattan_region = 'Uptown'
                    else:
                        manhattan_region = 'Harlem'
                    writer.writerow(
                        [restaurant_id, restaurant_name, cuisine_type, restaurant_address, latitude,
                         longitude, manhattan_region, restaurant_rating, review_count, price])



