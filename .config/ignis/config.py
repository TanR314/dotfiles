import os
from ignis.utils import Utils
from ignis.app import IgnisApp
app = IgnisApp.get_default()



app.add_icons(f"{Utils.get_current_dir()}/assets")



from windows.bar import Bar
from windows.notifications import NotificationPopup

NotificationPopup()


from windows.screen_corners import RoundCorners



app.apply_css(os.path.expanduser("~/.config/ignis/styles/main.scss"))




import wallpapers 




# from windows.overview_search import overview_search
