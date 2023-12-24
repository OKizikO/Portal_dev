from bs4 import BeautifulSoup as bs
from dotenv import load_dotenv
import requests
import json
import os

load_dotenv()

session = requests.Session()

payload = {
	'name': os.environ.get('user'),
	'pass': os.environ.get('passw'),
	'form_build_id': os.environ.get('fbid'),
	'form_id': os.environ.get('fi'),
	'op': os.environ.get('op')
}
s = session.post("https://myprimeportal.com/node?destination=node", data=payload)
s = session.get('https://www.myprimeportal.com/mystore')
full_html = bs(s.content, 'html.parser')
full_str = str(full_html)
with open('source/mystore.html', 'w', encoding='utf-8') as file:
	file.write(full_str)
	
store = full_html.find_all('div', class_='panel prime-storepage-alert')
store_str = str(store)
with open('source/alerts.html', 'w', encoding='utf-8') as file:
	file.write(store_str)
	
rates = full_html.find_all('div', class_='b10 text-center')
rates_str = str(rates)
with open('source/rates.html', 'w', encoding='utf-8') as file:
	file.write(rates_str)
	
rank = full_html.find_all('div', class_='panel widget-photoday prime-storepage-alert')
rank_str = str(rank)
with open('source/ranks.html', 'w', encoding='utf-8') as file:
	file.write(rank_str)

payload = {
	'mystoreid': 2132,
	'accordionis': 3
}
s = session.post("https://myprimeportal.com/storeaccordion/storepeople/", data=payload)
soup = bs(s.content, 'html.parser')
st = soup.prettify()
with open('source/people.html', 'w', encoding='utf-8') as file:
	file.write(st)
	
payload = {
	'mystoreid': 2132,
	'accordionid': 1
}
s = session.post("https://myprimeportal.com/storeaccordion/storesales/", data=payload)
soup = bs(s.content, 'html.parser')
st = soup.prettify()
with open('source/sales.html', 'w', encoding='utf-8') as file:
	file.write(st)

payload = {
	'mystoreid': 2132,
	'accordionid': 147
}
s = session.post("https://myprimeportal.com/storeaccordion/mtdtrendntogo", data=payload)
soup = bs(s.content, 'html.parser')
st = soup.prettify()
with open('source/trends.html', 'w', encoding='utf-8') as file:
	file.write(st)
	
s = session.post("https://myprimeportal.com/ssalesalert/ajax/2/2132")
soup = json.loads(s.content)
html_content = ""
for item in soup:
	if 'output' in item:
		html_content += item['output']
soup = bs(html_content, 'html.parser')
pretty_html = soup.prettify()
with open('source/psq.html', 'w', encoding='utf-8') as file:
	file.write(pretty_html)

s = session.post("https://myprimeportal.com/ssalesalert/ajax/9/2132")
soup = json.loads(s.content)
html_content = ""
for item in soup:
	if 'output' in item:
		html_content += item['output']
soup = bs(html_content, 'html.parser')
pretty_html = soup.prettify()
with open('source/plus1.html', 'w', encoding='utf-8') as file:
	file.write(pretty_html)

s = session.post("https://myprimeportal.com/ssalesalert/ajax/1/2132")
soup = json.loads(s.content)
html_content = ""
for item in soup:
	if 'output' in item:
		html_content += item['output']
soup = bs(html_content, 'html.parser')
pretty_html = soup.prettify()
with open('source/cru.html', 'w', encoding='utf-8') as file:
	file.write(pretty_html)
	
s = session.post("https://myprimeportal.com/ssalesalert/ajax/25/2132")
soup = json.loads(s.content)
html_content = ""
for item in soup:
	if 'output' in item:
		html_content += item['output']
soup = bs(html_content, 'html.parser')
pretty_html = soup.prettify()
with open('source/tv.html', 'w', encoding='utf-8') as file:
	file.write(pretty_html)

print('source files updated')
