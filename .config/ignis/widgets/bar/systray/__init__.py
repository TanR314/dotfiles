from ignis.widgets import Widget
from ignis.services.system_tray import SystemTrayService

system_tray = SystemTrayService.get_default()


class TrayItem(Widget.Button):
    def __init__(self, item):
        if item.menu:
            menu = item.menu.copy()
            menu.set_has_arrow(False)
        else:
            menu = None

        super().__init__(
            child=Widget.Box(
                css_classes=["tray-item"],
                child=[
                    Widget.Icon(image=item.bind("icon"), pixel_size=24),
                    menu,
                ]
            ),
            tooltip_text=item.bind("tooltip"),
            on_click=lambda x: item.activate(),
            on_right_click=lambda x: menu.popup() if menu else None,
            css_classes=["tray-item", "unset"],
        )

        item.connect("removed", lambda x: self.unparent())


class tray(Widget.Box):
    def __init__(self):
        super().__init__(
            css_classes=["tray"],
            setup=lambda self: system_tray.connect(
                "added", lambda x, item: self.append(TrayItem(item))
            ),
        )
