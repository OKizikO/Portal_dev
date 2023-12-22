from bs4 import BeautifulSoup as bs
from datetime import datetime
import pandas as pd
import json
import re

# init all html data gathered from get_source script
with open('source/alerts.html', 'r', encoding='utf-8') as file:
	alerts_data = file.read()
with open('source/mystore.html', 'r', encoding='utf-8') as file:
	mystore_data = file.read()
with open('source/people.html', 'r', encoding='utf-8') as file:
	people_data = file.read()
with open('source/psq.html', 'r', encoding='utf-8') as file:
	psq_data = file.read()
with open('source/ranks.html', 'r', encoding='utf-8') as file:
	ranks_data = file.read()
with open('source/rates.html', 'r', encoding='utf-8') as file:
	rates_data = file.read()
with open('source/sales.html', 'r', encoding='utf-8') as file:
	sales_data = file.read()
with open('source/trends.html', 'r', encoding='utf-8') as file:
	trends_data = file.read()

# gets the last updated date from the rates source file
def get_date():
	soup = bs(rates_data, 'html.parser')
	rates_str = str(soup)
	date_pattern = re.compile(r'\(Updated Thru: (\d{1,2}/\d{1,2}/\d{2,4})\)')
	match = date_pattern.search(rates_str)
	if match:
		date_str = match.group(1)
		return(date_str)
	else:
		print("Date not found.")
		
# gets tue total store alert count
def alert_count():
	soup = bs(alerts_data, 'html.parser')
	count = soup.find('h5', class_="f_attwhite", style="margin:0px;padding:2px;").text
	pattern = re.compile(r'\d+(\.\d+)?')
	match = pattern.search(count)
	if match:
		result = float(match.group())
		return(result)
	else:
		print('error: no alert data found!')
		return None  # Return None if no match is found
		
# gets the store district, market and company rank
def rankings():
	def extract_text(pattern, content):
		match = re.search(pattern, content, re.DOTALL)
		return match.group(1).strip() if match else None
	soup = bs(ranks_data, 'html.parser')
	text_content = soup.get_text(separator='\n', strip=True)
	district_pattern = r'District:(.*?)(?=Market:)'
	market_pattern = r'Market:(.*?)(?=Company:)'
	company_pattern = r'Company:(.*?)(?=RSM:)'
	district_text = extract_text(district_pattern, text_content)
	market_text = extract_text(market_pattern, text_content)
	company_text = extract_text(company_pattern, text_content)
	# Print the extracted text
	ranks = {
	'district': district_text,
	'market': market_text,
	'company': company_text
	}
	return(ranks)
	
# gets the store alert details
def alert_status():
	soup = bs(alerts_data, 'html.parser')
	sales_alerts = [
	{item.find('h4', class_='sender').text.strip():
	item.find('span', class_='label').text.strip() if item.find('span', class_='label') else 0}
	for item in soup.find_all('li')
	]
	result_dict = {}
	for entry in sales_alerts:
		key = next(iter(entry))
		value = entry[key]
		result_dict[key] = int(value) if value.isdigit() else 0
	return(result_dict)
	
# gets individual employee PSQ data
def psq():
	soup = bs(psq_data, 'html.parser')
	table = soup.find('table', {'id': 'marketopsalert_download_2_'})
	headers = [header.text.strip() for header in table.find_all('th')]
	rows = table.find_all('tr')[1:]
	data = []
	for row in rows:
		row_data = [cell.text.strip() for cell in row.find_all('td')]
		data.append(dict(zip(headers, row_data)))
	filtered_data = [
	{k: v for k, v in entry.items() if k.lower() not in ['vp', 'market', 'dm', 'store']}
	for entry in data
	]
	return(filtered_data)
	
# gets the stores 12 month historical sales data
def sales():
	soup = bs(sales_data, 'html.parser')
	table = soup.find('table', {'id': 'store_sales_dsr'})
	df = pd.read_html(str(table))[0]
	json_data = df.to_json(orient='records')
	return(json_data)
	
# gets the stores daily goal based on run rate
def rpd():
	soup = bs(trends_data, 'html.parser')
	text_content = soup.get_text(separator='\n', strip=True)
	input_text_cleaned = re.sub(r'\*.*', '', text_content, flags=re.DOTALL)
	req_day_values = re.findall(r'Req/Day\D*(\d+)', input_text_cleaned)
	categories = ['opps', 'ppvga', 'tv', 'bb', 'pa', 'ar']
	result_dict = dict(zip(categories, req_day_values))
	result_dict.pop('bb', None)
	result_dict.pop('pa', None)
	return(result_dict)
	
# gets the store csat and ppvga cancel rate
def csat():
	soup = bs(ranks_data, 'html.parser').text
	stripped = soup.replace(' ', '').replace('\n', '')
	csat_pattern = re.compile(r'CSAT(\d+\.\d+)%')
	ppvgacancel_pattern = re.compile(r'PPVGACancel%(\d+\.\d+)')
	csat_match = csat_pattern.search(stripped)
	ppvgacancel_match = ppvgacancel_pattern.search(stripped)
	result_dict = {
		"CSAT": float(csat_match.group(1)) if csat_match else None,
		"PPVGACANCEL": float(ppvgacancel_match.group(1)) if ppvgacancel_match else None
}
	return(result_dict)
		
# gets the stores run rates
def rates():
	soup = bs(rates_data, 'html.parser').text
	stripped = soup.replace('\n', '')
	index_opps_goal = stripped.find("OppsGoal")
	result = stripped[index_opps_goal:]
	index_protection_goal = result.find("ProtectionGoal: >=66%")
	result = result[:index_protection_goal + len("ProtectionGoal: >=66%")] + "PAMTD:" + result[index_protection_goal + len("ProtectionGoal: >=66%"):]
	result = result.replace('Launch Spotlight', '')
	modified_string = re.sub(r'(AccessoriesGoal: \$[\d,]+)', r'\1 AccRR:', result)
	modified_string = re.sub(r'(\d+%)(\d+%)', r'\1 RPMTD: \2', modified_string)
	modified_string = modified_string[:-1]
	strip = modified_string.replace('%','').replace(' ', '')
	pattern = re.compile(r'(\w+PPVGAYOYGoal:>=)(0*)(\d+\.?\d*)')
	modified_string = pattern.sub(r'\1\2 YOY:\3', strip)
	output_string = re.sub(r'(\d)([A-Za-z])', r'\1 \2', modified_string)
	output_string = output_string.replace('$', '').replace(',', '').replace(' ', ',').replace('Plus1,RR', 'Plus1RR')
	pairs = output_string.split(',')
	data_dict = {}
	for pair in pairs:
		key_value = pair.split(':')
		key = key_value[0]
		if len(key_value) > 1:
			value_str = key_value[1].strip()
			if '.' in value_str:
				value = float(value_str)
			elif value_str.isdigit() or (value_str[0] == '-' and value_str[1:].isdigit()):
				value = int(value_str)
			else:
				value = value_str
			data_dict[key] = value
		else:
			data_dict[key] = None
	return(data_dict)

# gets the stores UCR
def ucr():
	soup = bs(alerts_data, 'html.parser')
	table = soup.find('table')
	table_data = {}
	headers = []
	for row in table.find_all('tr'):
		columns = row.find_all(['td', 'th'])
		if not headers:
			headers = [header.text.strip() for header in columns]
		else:
			row_data = {}
			for i in range(len(columns)):
				row_data[headers[i]] = columns[i].text.strip()
			table_data[row_data[headers[0]]] = row_data
	upgrade_value = table_data['N/A']['Upgrade']
	upgrade_value = upgrade_value.replace('%', '')
	return(float(upgrade_value))




# gets the stores individual employeee sales data
def people():
	ct = 0
	fn = 'temp'
	soup = bs(people_data, 'html.parser')
	data = soup.find_all('div', class_='col-md-12 mb5')
	for i in data:
		data_str = str(i)
		with open(f'{fn+str(ct)}.html', 'w', encoding='utf-8') as file:
			file.write(data_str)
		ct += 1

	
	
	
	
	
	
# -----------------BUILDS THE JSON OUTPUT

'''
def build_output():
        date = get_date()
        alerts = alert_count()
        rank = rankings()
        ucrp = ucr()
        status = alert_status()
        psqs = psq()
        rrates = rates()
        reqpd = rpd()
        hist = sales()
        csats = csat()
        result = { date: {
                'alerts': alerts,
                'rank': rank,
                'ucr': ucrp,
                'status': status,
                'psq': psqs,
                'rates': rrates,
                'RPD': reqpd,
                'csat': csats,
                'historical': hist
                }
        }
        json_data = json.dumps(result, indent=2)
        print(json_data)

build_output()
'''

people()
