import requests

url = 'http://realtime.mbta.com/developer/api/v2'
payload = {'api_key': 'wX9NwuHnZU2ToO7GmGR9uw', 'format': 'json'}

# get commuter rail only routes
def routes():
    response_routes = requests.get(url + '/routes', params=payload)
    response_routes_parsed = response_routes.json()

    cr_routes = []
    for m in response_routes_parsed.get('mode'):
        if m.get('route_type') == "2":
            cr_routes = m.get('route')
            break

    return cr_routes
