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

# determine movement of kpis
alert_delta = round((current[current_date]['alerts'] - previous[previous_date]['alerts']),2)
ucr_delta = round((current[current_date]['ucr'] - previous[previous_date]['ucr']),2)
opps_delta = round((current[current_date]['rates']['OppsRR']-previous[previous_date]['rates']['OppsRR']),2)
vga_delta = round((current[current_date]['rates']['RR']-previous[previous_date]['rates']['RR']),2)


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

	
# ---------- UI ----------
		
# Summary View
def call_summary(sender):
    v = ui.ScrollView()
    width = v.width
    v.background_color = background
    v.name = 'Summary'
    # date header
    header = ui.Label(frame=(width-15,0,10,10), text_color=text_color, font=('ChalkboardSE-Bold', 20))
    header.text = f'Summary for {current_date}'
    header.size_to_fit()
    # metric data containers
    #opps
    opps_cont = ui.View(frame=(5,50,120,100), background_color=opps_color, corner_radius=20)
    opps_label = ui.Label(frame=(7.5,0,0,0), text_color=card_text, font=('ChalkboardSE-Regular',40))
    opps_label.text = 'OPPS'
    opps_label.size_to_fit()
    opps_cont.add_subview(opps_label)
    # vga
    vga_cont = ui.View(frame=(137.5,50,120,100), background_color=vga_color, corner_radius=20)
    vga_label = ui.Label(frame=(10,0,0,0), text_color=card_text, font=('ChalkboardSE-Regular',40))
    vga_label.text = 'VGAS'
    vga_label.size_to_fit()
    vga_cont.add_subview(vga_label)
    # ucr
    ucr_cont = ui.View(frame=(270,50,120,100), background_color=ucr_color, corner_radius=20)
    ucr_label = ui.Label(frame=(20,0,0,0), text_color=card_text, font=('ChalkboardSE-Regular',40))
    ucr_label.text = 'UCR'
    ucr_label.size_to_fit()
    ucr_cont.add_subview(ucr_label)
    # add subviews
    v.add_subview(header); v.add_subview(opps_cont); v.add_subview(vga_cont); v.add_subview(ucr_cont)
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

# navigation view controller
nav_view = ui.NavigationView(root_view, tint_color=tint)
nav_view.background_color = background
nav_view.present('fullscreen', hide_title_bar=True)
# 2 finger swipe down to close
