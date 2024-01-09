import ui
import os
import json

# ---------- LOGIC ----------

# load current and previous day from data
with open('data/full.json', 'r')as file:
	data = json.load(file)
	current = data[-1]
	current_date = next(iter(current))
	previous = data[-2]
	previous_date = next(iter(previous))


# ---------- KPIS ----------
# determine movement of kpis
alert_delta = round((current[current_date]['alerts'] - previous[previous_date]['alerts']),2)
ucr_delta = round((current[current_date]['ucr'] - previous[previous_date]['ucr']),2)
opps_delta = round((current[current_date]['rates']['OppsRR']-previous[previous_date]['rates']['OppsRR']),2)
vga_delta = round((current[current_date]['rates']['RR']-previous[previous_date]['rates']['RR']),2)


# ---------- Multiplier ----------
# takes a daily record and returns the multiplier for that record
def get_multi(rec):
	pass


# ---------- Colors ----------
# Determine if dark mode is on and set colors accordingly
dark_mode = ui.get_ui_style() == 'dark'
background = '2E2B2B' if dark_mode else 'EAEAEA'
tint = 'teal' if dark_mode else '4586FF'
text_color = 'white' if dark_mode else 'black'
card_color = '388186' if dark_mode else '00ADB5'
card_text = 'white' if dark_mode else 'black'
up = 'A8DF8E'
down = 'FFBFBF'
neutral = 'FFBFBF'
alert_color = down if alert_delta < 0 else neutral if alert_delta == 0 else up
ucr_color = down if ucr_delta < 0 else neutral if ucr_delta == 0 else up
opps_color = down if opps_delta < 0 else neutral if opps_delta == 0 else up
vga_color = down if vga_delta < 0 else neutral if vga_delta == 0 else up


# ---------- Fonts ----------
# set various fonts and sizes
header_font = ('ChalkboardSE-Bold', 20)
title_font = ('ChalkboardSE-Bold', 20)
numeral_font = ('ChalkboardSE-Regular', 30)
detail_font = ('ChalkboardSE-Regular', 14)


# ---------- UI VIEWS ----------
		
# Summary View
def call_summary(sender):
    v = ui.ScrollView()
    v.background_color = background
    v.name = 'Summary'
    
    # date header
    header_cont = ui.View(frame=(5,10,383,35), background_color='3fc1c9', corner_radius=15)
    header = ui.Label(frame=(0,0,header_cont.width,header_cont.height), text_color=text_color, font=header_font)
    header.text = f'Summary for {current_date}'
    header.alignment = ui.ALIGN_CENTER
    header_cont.add_subview(header)
    
    # Alerts Header
    # date header
    alert_cont = ui.View(frame=(5,55,383,35), background_color=alert_color, corner_radius=15)
    alert_label = ui.Label(frame=(0,0,alert_cont.width,alert_cont.height), text_color=text_color, font=header_font)
    alert_label.text = f'Alert Count: {int(current[current_date]["alerts"])}'
    alert_label.alignment = ui.ALIGN_CENTER
    alert_cont.add_subview(alert_label)
    alert_change = ui.Label(frame=(-10,0,alert_cont.width,alert_cont.height), text_color=text_color, font=detail_font)
    alert_change.text = f'Change: {alert_delta}'
    alert_change.alignment = ui.ALIGN_RIGHT
    alert_cont.add_subview(alert_change)
    
    # metric data containers
    #opps
    opps_cont = ui.View(frame=(5,100,120,100), background_color=opps_color, corner_radius=20)
    opps_label = ui.Label(frame=(0,0,opps_cont.width,40), text_color=card_text, font=title_font)
    opps_label.text = 'OPPS'
    opps_label.alignment = ui.ALIGN_CENTER
    opps_cont.add_subview(opps_label)
    opps_count = ui.Label(frame=(0,0,opps_cont.width,opps_cont.height), text_color=card_text, font=numeral_font)
    opps_count.text = f'{current[current_date]["rates"]["OppsRR"]}'
    opps_count.alignment = ui.ALIGN_CENTER
    opps_cont.add_subview(opps_count)
    opps_d = ui.Label(frame=(0,0,opps_cont.width,165), text_color=card_text, font=detail_font)
    opps_d.text = f'Change: {opps_delta}'
    opps_d.alignment = ui.ALIGN_CENTER
    opps_cont.add_subview(opps_d)
    # vga
    vga_cont = ui.View(frame=(137.5,100,120,100), background_color=vga_color, corner_radius=20)
    vga_label = ui.Label(frame=(0,0,vga_cont.width,40), text_color=card_text, font=title_font)
    vga_label.text = 'VGAS'
    vga_label.alignment = ui.ALIGN_CENTER
    vga_cont.add_subview(vga_label)
    vga_count = ui.Label(frame=(0,0,vga_cont.width,vga_cont.height), text_color=card_text, font=numeral_font)
    vga_count.text = f'{current[current_date]["rates"]["RR"]}'
    vga_count.alignment = ui.ALIGN_CENTER
    vga_cont.add_subview(vga_count)
    vga_d = ui.Label(frame=(0,0,vga_cont.width,165), text_color=card_text, font=detail_font)
    vga_d.text = f'Change: {vga_delta}'
    vga_d.alignment = ui.ALIGN_CENTER
    vga_cont.add_subview(vga_d)
    # ucr
    ucr_cont = ui.View(frame=(270,100,120,100), background_color=ucr_color, corner_radius=20)
    ucr_label = ui.Label(frame=(0,0,ucr_cont.width,40), text_color=card_text, font=title_font)
    ucr_label.text = 'UCR'
    ucr_label.alignment = ui.ALIGN_CENTER
    ucr_cont.add_subview(ucr_label)
    ucr_count = ui.Label(frame=(0,0,ucr_cont.width,ucr_cont.height), text_color=card_text, font=numeral_font)
    ucr_count.text = f'{current[current_date]["ucr"]}'
    ucr_count.alignment = ui.ALIGN_CENTER
    ucr_cont.add_subview(ucr_count)
    ucr_d = ui.Label(frame=(0,0,ucr_cont.width,165), text_color=card_text, font=detail_font)
    ucr_d.text = f'Change: {ucr_delta}'
    ucr_d.alignment = ui.ALIGN_CENTER
    ucr_cont.add_subview(ucr_d)
    
    # add subviews
    v.add_subview(header_cont); v.add_subview(alert_cont); v.add_subview(opps_cont); v.add_subview(vga_cont); v.add_subview(ucr_cont)
    sender.navigation_view.push_view(v)


# People View
def call_people(sender):
    v = ui.ScrollView()
    v.background_color = background
    v.name = 'People'
    sender.navigation_view.push_view(v)


# Sales View
def call_sales(sender):
    v = ui.ScrollView()
    v.background_color = background
    v.name = 'Sales'
    sender.navigation_view.push_view(v)


# Historical View
def call_historic(sender):
    v = ui.ScrollView()
    v.background_color = background
    v.name = 'Historic'
    sender.navigation_view.push_view(v)


# Projections View
def call_projections(sender):
    v = ui.ScrollView()
    v.background_color = background
    v.name = 'Projections'
    sender.navigation_view.push_view(v)


# Root view
def call_root():
	root_view = ui.ScrollView()
	root_view.background_color = background
	root_view.name = 'Portal Data'
	# Add logo image to root view
	logo_path = 'assets/logo.png'
	logo_image = ui.Image.named(logo_path)
	logo_view = ui.ImageView(frame=(65, 0, 250, 100))
	logo_view.image = logo_image
	root_view.add_subview(logo_view)
	# Summary Button
	summary_button = ui.Button(title='Summary', frame=(10,110,150,150), font=('ChalkboardSE-Regular', 20), tint_color=tint)
	summary_button.action = call_summary 
	root_view.add_subview(summary_button)
	# People Button
	people_button = ui.Button(title='People', frame=(10,150,150,150), font=('ChalkboardSE-Regular', 20), tint_color=tint)
	people_button.action = call_people 
	root_view.add_subview(people_button)
	# Sales Button
	sales_button = ui.Button(title='Sales', frame=(10,190,150,150), font=('ChalkboardSE-Regular', 20), tint_color=tint)
	sales_button.action = call_sales 
	root_view.add_subview(sales_button)
	# Historic Button
	historic_button = ui.Button(title='Historic', frame=(10,230,150,150), font=('ChalkboardSE-Regular', 20), tint_color=tint)
	historic_button.action = call_historic 
	root_view.add_subview(historic_button)
	# Projections Button
	proj_button = ui.Button(title='Projections', frame=(10,270,150,150), font=('ChalkboardSE-Regular', 20), tint_color=tint)
	proj_button.action = call_projections
	root_view.add_subview(proj_button)
	return root_view


root = call_root()
# ---------- navigation view controller ----------
nav_view = ui.NavigationView(root, tint_color=tint)
nav_view.background_color = background
nav_view.present('fullscreen', hide_title_bar=True)
# 2 finger swipe down to close
