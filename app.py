import ui
import os

# Determine if dark mode is on amd set colors accordingly
dark_mode = ui.get_ui_style() == 'dark'
background = 'black' if dark_mode else 'white'
tint = 'teal' if dark_mode else 'turquoise'

		
# Summary View
def call_summary(sender):
    v = ui.ScrollView()
    v.background_color = background
    v.name = 'Summary'
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
logo_view = ui.ImageView(frame=(120, 0, 150, 100))
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


nav_view = ui.NavigationView(root_view, tint_color=tint)
nav_view.background_color = background
nav_view.present('fullscreen', hide_title_bar=True)
# 2 finger swipe down to close
