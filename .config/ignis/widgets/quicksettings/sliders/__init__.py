from ignis.widgets import Widget
# from widgets.bar.stackright.audio import AudioIndicator


from ignis.services.audio import AudioService
audio = AudioService.get_default()
from ignis.services.backlight import BacklightService
backlight = BacklightService.get_default()





# Audio 

def AudioIcon():
    return Widget.Icon(
        css_classes=["quicksettings-slider-icon"],
        image=audio.speaker.bind("icon_name")
    )

def speaker_slider() -> Widget.Scale:
    return Widget.Scale(
        min=0,
        max=100,
        step=1,
        hexpand=True,
        value=audio.speaker.bind("volume", lambda x: x if x != None else 20),
        on_change=lambda x: audio.speaker.set_volume(x.value),
        css_classes=["slider"],  # we will customize style in style.css
        sensitive=True
    )



def AudioWidget():
    return Widget.Box(
        css_classes=["quicksettings-slider"],
        child=[
            AudioIcon(),
            speaker_slider(),
        ]
    )





# Brightness


def brightnessChange(x):
    backlight.devices[0].set_brightness(backlight.max_brightness * x.value / 100)


def brightnessIcon():
    return Widget.Icon(
        css_classes=["quicksettings-slider-icon"],
        image="display-brightness-symbolic"
    )

def brightness_slider() -> Widget.Scale:
    return Widget.Scale(
        min=0,
        max=100,
        step=1,
        hexpand=True,
        value=backlight.bind("brightness", lambda x: x/backlight.max_brightness * 100 if x != None else 20),
        on_change = brightnessChange,
        css_classes=["brightness-slider", "slider"],  # we will customize style in style.css
    )

def BrightnessWidget():
    return Widget.Box(
        css_classes=["quicksettings-slider"],
        child=[
            brightnessIcon(),
            brightness_slider(),
        ]
    )
