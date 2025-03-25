from ignis.widgets import Widget
from widgets.bar.dateButton import DateButton
from widgets.bar.stackright import StackRight
from widgets.bar.workspaces import Workspaces
from widgets.bar.systray import tray
from widgets.bar.battery import Battery


from ignis.services.fetch import FetchService

fetch = FetchService.get_default()


Bar = Widget.Window(
    namespace="bar",
    exclusivity="exclusive",
    # exclusivity="normal",
    anchor=["top","left","right"],
    layer="top",
    child=Widget.CenterBox(
        css_classes=["bar", "window"],
        start_widget = Widget.Box(
            child=[
                Widget.Icon(
                    image=fetch.os_logo,
                    pixel_size=24,
                    style="margin-right: 8px;" 
                ),
                # Workspaces()
            ]
        ),
        center_widget = Widget.Box(
            child=[
                DateButton()
            ]
        ),
        end_widget = Widget.Box(
            child=[
                tray(),
                StackRight(),
                Battery()
            ]
        )
        
    ),
)
