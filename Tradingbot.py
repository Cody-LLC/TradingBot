from coinbase.rest import RESTClient
import json
from json import dumps
from coinbase.websocket import WSClient
import time
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")
client = RESTClient(api_key=api_key, api_secret=api_secret)

print(f"API Key Length: {len(api_key)}")
print(f"API Secret Length: {len(api_secret)}")

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


