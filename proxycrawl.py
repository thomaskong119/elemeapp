from urllib.parse import quote_plus
from urllib.request import urlopen

url = quote_plus('https://www.ele.me/shop/764140')

handler = urlopen('https://api.proxycrawl.com/?token=BgGGVdz-J9J6FUKHbiy7mA&url=' + url)

print(handler.read())