#!/usr/bin/env python3
"""
Python module to generate an alert if a currency's current price
is more than one standard deviation from the 24hr average
"""

import sys
import argparse
from datetime import datetime, timezone
import json
import pprint
import requests

def get_symbols():
    """Retrieves all available symbols for trading"""
    base_url = "https://api.gemini.com/v1"
    response = requests.get(base_url + "/symbols")
    return response.json()

def get_prices(currency):
    """Retrieves information about recent trading activity for the provided currency"""
    base_url = "https://api.gemini.com/v2"
    response = requests.get(base_url + "/ticker/" + currency)
    return response.text

def average(num_list):
    """Takes in a list num_list, returns the average of num_list"""
    return sum(num_list) / len(num_list)

def main():
    """Gathers information about a symbol, calculates relevant values, outputs JSON alert"""
    # Get price info and Parse JSON into object with attributes corresponding to dict keys
    price_info = json.loads(get_prices(args.currency))

    # Calculate values
    close   = float(price_info['close'])
    # Convert list of strings to floats
    changes = list(map(lambda price: float(price.replace(",", "")), price_info['changes']))
    avg     = average(changes)
    change  = avg - close
    sdev    = (change / avg) * 100

    # Generate alert if current price > than {args.deviation} standard dev from 24hr average
    if sdev > float(args.deviation):
        # Structure alert
        output = {}
        output['timestamp']          = datetime.utcnow().replace(tzinfo=timezone.utc).isoformat()
        output['level']              = 'INFO'
        output['trading_pair']       = args.currency
        output['deviation']          = True
        output['data']               = {}
        output['data']['last_price'] = f'{close:.2f}'
        output['data']['average']    = f'{avg:.2f}'
        output['data']['change']     = f'{change:.2f}'
        output['data']['sdev']       = f'{sdev:.2f}'

        # Convert data dict to JSON and print
        json_data = json.dumps(output)
        print(json_data)


# Create a parser and add arguments
parser = argparse.ArgumentParser(description='Runs checks on API')
parser.add_argument('-c', '--currency', default='btcusd', help='The currency trading pair, or ALL')
parser.add_argument('-d', '--deviation', default=1, help='percentage threshold for deviation')
parser.add_argument('-s', '--symbols', action='store_true', help='list available trading pairs')

# Parse the arguments
args = parser.parse_args()

# List available currency trading pairs if symbols flag passed
if args.symbols:
    symbols = get_symbols()
    print('Available currency trading pairs:')
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(symbols)
    sys.exit()

if __name__ == "__main__":
    main()
