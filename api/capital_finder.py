import requests
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        query_params = parse_qs(urlparse(self.path).query)

        if 'country' in query_params:
            country_name = query_params['country'][0]
            capital = self.get_capital_by_country(country_name)
            response_message = f"The capital of {country_name} is {capital}"
        elif 'capital' in query_params:
            capital_name = query_params['capital'][0]
            country = self.get_country_by_capital(capital_name)
            response_message = f"{capital_name} is the capital of {country}"
        else:
            response_message = "Please provide a country or a capital"

        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.end_headers()
        self.wfile.write(response_message.encode('utf-8'))
        return
    
    def get_capital_by_country(self, country_name):
        url = f"https://restcountries.com/v3.1/name/{country_name}?fields=name,capital"
        response = requests.get(url)
        data = response.json()
        return data[0]['capital'][0]
    
    def get_country_by_capital(self, capital_name):
        url = f"https://restcountries.com/v3.1/capital/{capital_name}?fields=name"
        response = requests.get(url)
        data = response.json()
        return data[0]['name']['common']
    