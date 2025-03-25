from ignis.widgets import Widget
from ignis.services.upower import UPowerService, UPowerDevice

upower = UPowerService.get_default()



def setupBatteries(widget):
    def update(battery):
        charge = battery.percent
        warning = 30
        chargeForBar = int(((charge+5) // 10) * 10)
        if battery.charging:
            iconName = "battery-flash-symbolic"
            widget.child[0].image = iconName
            barName = "battery-level-" + str(chargeForBar)
            if charge <= warning:
                widget.child[0].css_classes = ["battery-icon", "battery-level-"+str(chargeForBar), "charging", "low"]
                widget.child[1].css_classes = ["battery-bar", barName, "charging", "low"]
            else:
                widget.child[0].css_classes = ["battery-icon", "battery-level-"+str(chargeForBar), "charging"]
                widget.child[1].css_classes = ["battery-bar", barName, "charging"]
        else:
            iconName = "battery-level-" + str(chargeForBar) + "-symbolic"
            widget.child[0].image = iconName
            barName = "battery-level-" + str(chargeForBar)
            if charge <= warning:
                widget.child[0].css_classes = ["battery-icon", "battery-level-"+str(chargeForBar), "low"]
                widget.child[1].css_classes = ["battery-bar", barName, "low"]
            else:
                widget.child[0].css_classes = ["battery-icon", "battery-level-"+str(chargeForBar)]
                widget.child[1].css_classes = ["battery-bar", barName]


    update(upower.display_device)
    upower.display_device.connect(
        "notify::charging",
        lambda x,y: update(x)
    )
    upower.display_device.connect(
        "notify::percent",
        lambda x,y: update(x)
    )


class Battery(Widget.Box):
    def __init__(self):
        super().__init__(
            valign="center",
            halign="center",
            css_classes=["Battery"],
            child=[
                Widget.Icon(valign="center",halign="center",css_classes=["battery-icon"], pixel_size=18),
                Widget.Box(
                    valign="center",
                    overflow=True,
                    child=[
                        Widget.Box(valign="center",halign="center", css_classes=["block"]),
                    ],
                )
            ],
            setup=setupBatteries
        )
