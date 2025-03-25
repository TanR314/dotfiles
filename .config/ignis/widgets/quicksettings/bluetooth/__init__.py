from ignis.widgets import Widget
from ignis.services.bluetooth import BluetoothService

bluetooth = BluetoothService.get_default()






def BluetoothWidget():
    MyWifiList=Widget.Box(
        vertical=True,
        child=[
            Widget.Label(label=bluetooth.bind("state")),
            Widget.Label(label=bluetooth.bind("setup_mode", lambda x: "yes" if x else "no" )),
            Widget.Box(
                # child=bluetooth.bind(
                #     "state"
                # )
            )
        ]
    )

    def on_click(self):
        print("bruh")


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
    
