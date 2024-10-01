from coinbase.rest import RESTClient
import json
from json import dumps
from coinbase.websocket import WSClient
import time

api_key = "organizations/0eaca027-a715-4549-bada-629c487e301b/apiKeys/9ad625c0-c118-41fb-9b1c-af302f72543e"
api_secret = "-----BEGIN EC PRIVATE KEY-----\nMHcCAQEEIHun1+c0389CZougbNwfNlg8AVqwnuh484ORvsMVimVyoAoGCCqGSM49\nAwEHoUQDQgAEpAXteILICcCNQutzGFNOFMZPMukc2gvvVci8Y7W51l2coCar2GwZ\nMXj1BIinyzRpiDpxfGDAV/vp+7ZKzmczwg==\n-----END EC PRIVATE KEY-----\n"

client = RESTClient(api_key=api_key, api_secret=api_secret)

lowest_price = float('inf')  # Initialize to a high value
last_print_time = 0           # Time of the last print

def on_message(msg):
    global lowest_price, last_print_time
    data = json.loads(msg)
    
    try:
        price = float(data['events'][0]['tickers'][0]['price'])
        current_time = time.time() #current time
        if current_time - last_print_time > 0.25:  # Check if at least 0.5 seconds (2 times a second) have passed
            print(price)
            last_print_time = current_time
            if price < lowest_price: # Update the lowest price if the current price is lower
                lowest_price = price
                print(f"New Lowest Price: {lowest_price}")

    except (KeyError, IndexError) as e:
        print(f"Error retrieving price: {e}")



ws_client = WSClient(api_key=api_key, api_secret=api_secret, on_message=on_message, verbose=True)
ws_client.open()
ws_client.subscribe(["BTC-USD"], ["ticker"])
ws_client.run_forever_with_exception_check()


