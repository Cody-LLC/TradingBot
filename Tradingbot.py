from coinbase.rest import RESTClient
import json
from coinbase.websocket import WSClient
import time
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")
client = RESTClient(api_key=api_key, api_secret=api_secret)

lowest_price = float('inf')  # Initialize to a high value
highest_price = float('-inf')  # Initialize to a low value
last_print_time = 0           # Time of the last print
last_liquidity_check_time = 0  # Time of the last liquidity check
previous_lows = []            # Store previous lows for liquidity analysis
previous_highs = []           # Store previous highs for liquidity analysis

def process_price_data(price):
    global lowest_price, highest_price, last_print_time, last_liquidity_check_time, previous_lows, previous_highs

    current_time = time.time()  # Current time
    if current_time - last_print_time > 0.5:  # Limit the print rate
        print(price)
        last_print_time = current_time
        
        # Update the lowest price if the current price is lower
        if price < lowest_price:
            previous_lows.append(lowest_price)  # Save the previous lowest
            lowest_price = price
            print(f"New Lowest Price: {lowest_price}")
        
        # Check for liquidity sweeps on the lows if 15 minutes have passed
        if current_time - last_liquidity_check_time > 10:  # 15 minutes in seconds
            if previous_lows and price < min(previous_lows):  # If the price is below the last low
                print("Liquidity Sweep Detected (Low)")
            last_liquidity_check_time = current_time  # Update the last liquidity check time

        # Update the highest price if the current price is higher
        if price > highest_price:
            previous_highs.append(highest_price)  # Save the previous highest
            highest_price = price
            print(f"New Highest Price: {highest_price}")
        
        # Check for liquidity sweeps on the highs if 15 minutes have passed
        if current_time - last_liquidity_check_time > 10:  # 15 minutes in seconds
            if previous_highs and price > max(previous_highs):  # If the price is above the last high
                print("Liquidity Sweep Detected (High)")
            last_liquidity_check_time = current_time  # Update the last liquidity check time

def on_message(msg):
    data = json.loads(msg)
    try:
        price = float(data['events'][0]['tickers'][0]['price'])
        process_price_data(price)
    except (KeyError, IndexError) as e:
        print(f"Error retrieving price: {e}")

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
