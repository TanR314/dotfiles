from ignis.widgets import Widget

from ignis.services.audio import AudioService

audio = AudioService.get_default()



def AudioIndicator():
    return Widget.Icon(
        image=audio.speaker.bind("icon_name")
    )
