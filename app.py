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

# Determine if dark mode is on amd set colors accordingly
dark_mode = ui.get_ui_style() == 'dark'
background = '36393f' if dark_mode else 'f9f9f9'
tint = 'teal' if dark_mode else 'turquoise'
text_color = 'white' if dark_mode else 'black'
card_color = 'white' if dark_mode else 'white'
up_color = 'green'
down_color = 'red'

	
# ---------- UI ----------
		
# Summary View
def call_summary(sender):
    v = ui.ScrollView()
    width = v.width
    v.background_color = background
    v.name = 'Summary'
    # date header
    header = ui.Label(frame=(width-10,0,10,10), text_color=text_color, font=('ChalkboardSE-Bold', 20))
    header.text = f'Summary for {current_date}'
    header.size_to_fit()
    # metric data containers
    opps_cont = ui.View(frame=(10,50,120,100), background_color=card_color, corner_radius=10)
    vga_cont = ui.View(frame=(135,50,120,100), background_color=card_color, corner_radius=10)
    ucr_cont = ui.View(frame=(260,50,120,100), background_color=card_color, corner_radius=10)
    v.add_subview(header); v.add_subview(opps_cont); v.add_subview(vga_cont); v.add_subview(ucr_cont)
    sender.navigation_view.push_view(v)


# People View
def call_people(sender):
    v = ui.ScrollView()
    v.background_color = background
    v.name = 'People'
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
summary_button = ui.Button(title='Summary', frame=(10,100,150,150), font=('ChalkboardSE-Regular', 20), tint_color=tint)
summary_button.action = call_summary 
root_view.add_subview(summary_button)
# People Button
people_button = ui.Button(title='People', frame=(10,130,150,150), font=('ChalkboardSE-Regular', 20), tint_color=tint)
people_button.action = call_people 
root_view.add_subview(people_button)

# navigation view controller
nav_view = ui.NavigationView(root_view, tint_color=tint)
nav_view.background_color = background
nav_view.present('fullscreen', hide_title_bar=True)
# 2 finger swipe down to close
