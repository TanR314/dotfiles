from ignis.widgets import Widget
from ignis.services.network import NetworkService, WifiAccessPoint

network = NetworkService.get_default()



class AccessWidget(Widget.Button):
    def __init__(self, access_point):

        # self.

        super().__init__(
            child=Widget.Label(label=access_point.ssid),
            # on_click=lambda x: access_point.connect_to_graphical()
            on_click=lambda x: access_point.connect_to("HXAYbuUc")
        )





def NetworkWidget():
    MyWifiList=Widget.Box(
        vertical=True,
        child=[
            # Widget.Label(label=access_point.ssid)
            AccessWidget(access_point)
            for device in network.wifi.devices 
            for access_point in device.access_points
        ]
    )

    

            # for access_point in device.access_points
    # network.wifi.devices[0].scan()
    def on_click(self):
        network.wifi.devices[0].scan()
        for device in network.wifi.devices:
            for access_point in device.access_points:
                print(access_point.ssid)
        MyWifiList.child=[
            # Widget.Label(label=access_point.ssid)

            AccessWidget(access_point)
            for device in network.wifi.devices 
            for access_point in device.access_points
        ]
    # print(network.wifi.devices[0].access_points[1].ssid)


    return Widget.Box(
        vertical=True,
        child=[
            Widget.Button(
                label="Click Me",
                on_click=on_click
            ),
            MyWifiList,
        ]
    )
    
