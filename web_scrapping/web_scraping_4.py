from bs4 import BeautifulSoup
import requests

url = "https://coinmarketcap.com/"
result = requests.get(url).text
doc = BeautifulSoup(result, "html.parser")

tbody = doc.tbody
#print(tbody)

trs = tbody.contents
#print(trs)
#print(trs[0].next_sibling)
print(list(trs[0].next_siblings))
prices = {}

for tr in trs[:10]:
	name, price = tr.contents[2:4]
	fixed_name = name.p.string
	fixed_price = price.span.string

	prices[fixed_name] = fixed_price

print(prices)
#	name, price = tr.contents[2:4]
#	fixed_name = name.p.string
#	fixed_price = price.a.string

#	prices[fixed_name] = fixed_price

#print(prices)