import requests


def get_price():
  resp = requests.get('https://api.kraken.com/0/public/Ticker?pair=XBTUSD')

  return '${:,.2f}'.format(float(resp.json()["result"]['XXBTZUSD']['a'][0]))
