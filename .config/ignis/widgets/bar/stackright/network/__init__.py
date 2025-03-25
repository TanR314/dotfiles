from ignis.widgets import Widget

from ignis.services.network import NetworkService

network = NetworkService.get_default()



def WifiIndicator():
    return Widget.Icon(
        image=network.wifi.bind("icon_name")
    )

def EthernetIndicator():
    return Widget.Icon(
        image=network.ethernet.bind("icon_name")
    )

def NetworkIndicator():
    return Widget.Box(
        child=[
            WifiIndicator(),
            # EthernetIndicator()
        ]
    )
