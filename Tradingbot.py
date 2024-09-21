from coinbase.rest import REST.client
from json import dumps

api_key = "organizations/0eaca027-a715-4549-bada-629c487e301b/apiKeys/9ad625c0-c118-41fb-9b1c-af302f72543e"
api_secret = "-----BEGIN EC PRIVATE KEY-----\nMHcCAQEEIHun1+c0389CZougbNwfNlg8AVqwnuh484ORvsMVimVyoAoGCCqGSM49\nAwEHoUQDQgAEpAXteILICcCNQutzGFNOFMZPMukc2gvvVci8Y7W51l2coCar2GwZ\nMXj1BIinyzRpiDpxfGDAV/vp+7ZKzmczwg==\n-----END EC PRIVATE KEY-----\n"

client = RESTClient(api_key=api_key, api_secret=api_secret)
