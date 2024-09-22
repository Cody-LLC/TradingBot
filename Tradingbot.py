from coinbase.rest import RESTClient
from json import dumps
from coinbase.websocket import WSClient

api_key = "organizations/0eaca027-a715-4549-bada-629c487e301b/apiKeys/9ad625c0-c118-41fb-9b1c-af302f72543e"
api_secret = "-----BEGIN EC PRIVATE KEY-----\nMHcCAQEEIHun1+c0389CZougbNwfNlg8AVqwnuh484ORvsMVimVyoAoGCCqGSM49\nAwEHoUQDQgAEpAXteILICcCNQutzGFNOFMZPMukc2gvvVci8Y7W51l2coCar2GwZ\nMXj1BIinyzRpiDpxfGDAV/vp+7ZKzmczwg==\n-----END EC PRIVATE KEY-----\n"

client = RESTClient(api_key=api_key, api_secret=api_secret)
def on_message(msg):
    print(msg)
ws_client = WSClient(api_key=api_key, api_secret=api_secret, on_message=on_message, verbose=True)
ws_client.open()

ws_client.subscribe(["BTC-USD"], ["heartbeats", "ticker"])
ws_client.sleep_with_exception_check(10)
ws_client.close()