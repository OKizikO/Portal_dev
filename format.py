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
		
# gets the total store alert count
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
		for col_index, value in enumerate(row_data):
			try:
				row_data[col_index] = float(value)
			except ValueError:
				pass
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
	req_day_values = [float(value) for value in re.findall(r'Req/Day\D*(\d+)', input_text_cleaned)]
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
	modified_string = modified_string.replace('RR', 'OppsRR', 1)
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
	with open('source/cru.html', 'r') as file:
		data = file.read()
	soup = bs(data, 'html.parser')
	table = soup.find('table', {'class': 'table table-hover table-primary table-sm table-condensed tbl-slarge-font'})
	rows = table.find_all('tr')
	cru_goal = 0
	for row in rows[1:]:  
		columns = row.find_all('td')
		cru_goal = float(columns[9].get_text(strip=True))
	with open('source/tv.html', 'r') as file:
		data = file.read()
	soup = bs(data, 'html.parser')
	table = soup.find('table', {'class': 'table table-hover table-primary table-sm table-condensed tbl-slarge-font'})
	rows = table.find_all('tr')
	tv_goal = 0
	for row in rows[1:]:  
		columns = row.find_all('td')
		tv_goal = float(columns[9].get_text(strip=True))
	with open('source/plus1.html', 'r') as file:
		data = file.read()
	soup = bs(data, 'html.parser')
	table = soup.find('table', {'class': 'table table-hover table-primary table-sm table-condensed tbl-slarge-font'})
	rows = table.find_all('tr')
	plus1_goal = 0
	for row in rows[1:]:  
		columns = row.find_all('td')
		plus1_goal = float(columns[8].get_text(strip=True))
	data_dict['crugoal'] = cru_goal
	data_dict['tvgoal'] = tv_goal
	data_dict['plus1goal'] = plus1_goal
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
	people = []
	soup = bs(people_data, 'html.parser')
	data = soup.find_all('div', class_='col-md-12 mb5')
	data.pop(0)
	for i in data:
		data_str = str(i)
		data_str = data_str.replace('\n', '')
		soup = bs(data_str, 'html.parser')
		employee = soup.find('p', class_='title-sender').text
		employee = employee.replace('Date:', '')
		words = employee.split()
		first_name = words[0]
		last_name = words[1]
		emp_name = first_name +' '+ last_name
		title = words[2]
		hire_date = " ".join(words[4:])
		updated = soup.find('h3', class_="panel-title align-middle").text
		updated_on = re.findall(r'\((.*?)\)', updated)
		pattern = r'\d{1,2}/\d{1,2}/\d{2,4}'
		match = re.search(pattern, str(updated_on))
		if match:
			extracted_date = match.group()
		else:
			print("No date found.")
		ranks = soup.find_all('div', class_='col-sm-6')
		district_rank = ranks[0].text
		split_string = district_rank.split(':')
		if len(split_string) > 1:
			district_rank = split_string[1].strip()
		else:
			print("Colon not found in the district string.")
		market_rank = ranks[1].text
		split_string = market_rank.split(':')
		if len(split_string) > 1:
			market_rank = split_string[1].strip()
		else:
			print("Colon not found in the market string.")
		boxes = soup.find_all('div', class_='col-sm-2')
		opps = boxes[0].text
		opps = opps.replace('\n', '').replace(' ', '').replace('%', ' ').replace('H.Risk', 'HighRisk').replace('Plus1s:', 'PlusOne:')
		opps = re.sub(r'(\d+)([A-Za-z])', r'\1 \2', opps)
		key_value_pairs = re.findall(r'(\w+):(\S+)', opps)
		opps_dict = dict(key_value_pairs)
		prem = boxes[1].text
		prem = prem.replace(' ', '')
		prem = re.sub(r'(\d+)([A-Za-z])', r'\1 \2', prem)
		key_value_pairs = re.findall(r'(\w+):(\S+)', prem)
		prem_dict = dict(key_value_pairs)
		cru = boxes[2].text
		cru = cru.replace(' ', '')
		cru = re.sub(r'(\d+)([A-Za-z])', r'\1 \2', cru)
		key_value_pairs = re.findall(r'(\w+):(\S+)', cru)
		cru_dict = dict(key_value_pairs)
		pa = boxes[3].text
		pa = pa.replace(' ', '').replace('ProtectionGoal:65%', 'ProtectionGoal:65%PARR:').replace('%', '')
		pa = re.sub(r'(\d+)([A-Za-z])', r'\1 \2', pa)
		key_value_pairs = re.findall(r'(\w+):(\S+)', pa)
		pa_dict = dict(key_value_pairs)
		ar = boxes[4].text
		ar = ar.replace(' ', '')
		pattern = re.compile(r'(?<=\$)([\d,]+)(?=\$)')
		ar = pattern.sub(r'$\1ACRR:', ar)
		ar = ar.replace('$', '').replace(',', '')
		ar = re.sub(r'(\d+)([A-Za-z])', r'\1 \2', ar)
		key_value_pairs = re.findall(r'(\w+):(\S+)', ar)
		ar_dict = dict(key_value_pairs)
		rpm = boxes[5].text
		rpm = rpm.replace('%', '').replace(' ', '').replace('RatePlanGoal:88', 'RatePlanGoal:88RPMRR:')
		rpm = re.sub(r'(\d+)([A-Za-z])', r'\1 \2', rpm)
		key_value_pairs = re.findall(r'(\w+):(\S+)', rpm)
		rpm_dict = dict(key_value_pairs)
		output = {emp_name:{
		'title': title,
		'hired': hire_date,
		'updated': extracted_date,
		'district': district_rank,
		'market': market_rank,
		'opps': opps_dict,
		'prem': prem_dict,
		'cru': cru_dict,
		'pa': pa_dict,
		'ar': ar_dict,
		'rpm': rpm_dict
		}}
		people.append(output)
	def convert_to_float(result):
		if isinstance(result, dict):
			for key, value in result.items():
				result[key] = convert_to_float(value)
		elif isinstance(result, list):
			result = [convert_to_float(item) for item in result]
		elif isinstance(result, str) and result.isdigit():
			result = float(result)
		return(result)
	converted_data = convert_to_float(people)
	return(converted_data)
	
# gets all employee ci lead data
def cileads():
	soup = bs(alerts_data, 'html.parser')
	table = soup.find('table', {'id': 'cileadsmodalboxdetail'})
	headers = [header.text.strip() for header in table.find_all('th')]
	rows = []
	for row in table.find_all('tr')[1:]:
		row_data = [data.text.strip() for data in row.find_all('td')]
		rows.append(row_data)
	df = pd.DataFrame(rows, columns=headers)
	json_data = df.to_json(orient='records', indent=2)
	json_dict = json.loads(json_data)
	for i in json_dict:
		del i['Region']
		del i['Market']
		del i['DM']
		del i['Location']
	def convert_to_float(value):
		try:
			return float(value)
		except ValueError:
			return value
	converted_data = [{key: convert_to_float(value) for key, value in entry.items()} for entry in json_dict]
	return(converted_data)



# -----------------BUILDS THE JSON OUTPUT

def build_output():
        date = get_date()
        alerts = alert_count()
        rank = rankings()
        ucrp = ucr()
        status = alert_status()
        psqs = psq()
        lds = cileads()
        rrates = rates()
        reqpd = rpd()
        hist = sales()
        csats = csat()
        ppl = people()
        result = { date: {
                'alerts': alerts,
                'rank': rank,
                'ucr': ucrp,
                'status': status,
                'psq': psqs,
                'leads': lds,
                'rates': rrates,
                'RPD': reqpd,
                'csat': csats,
                'people': ppl,
                'historical': hist
                }
        }
        json_data = json.dumps(result)
        return(json_data)

data = build_output()
with open('data/daily.json', 'w') as file:
	json.dump(data, file)

print('File Saved')
