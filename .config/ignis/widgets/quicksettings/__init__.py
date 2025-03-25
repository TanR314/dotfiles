from ignis.widgets import Widget
from widgets.quicksettings.sliders import AudioWidget 
from widgets.quicksettings.sliders import BrightnessWidget 
from widgets.quicksettings.media import MediaPlayer 
from widgets.quicksettings.bluetooth import BluetoothWidget



def Quicksettings():
    return Widget.Box(
        css_classes=["quicksettings"],
        vertical=True,
        child=[
            Widget.Box(
                vertical=True,
                css_classes=["quicksettings-container"],
                child=[
                    AudioWidget(),
                    BrightnessWidget(),
                ]
            ),
            MediaPlayer(),
        ]
    )

