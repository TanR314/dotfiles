from ignis.widgets import Widget
from ignis.utils import Utils
from ignis.services.mpris import MprisService
from gi.repository import Gio

mpris = MprisService.get_default()

from .player_widget import MyPlayer
from utils.funcs import AddBox, RemoveAddedBox


class Popup(Widget.Box):
    def __init__(self, player):
        super().__init__(
            halign="center",
            child=[
                MyPlayer(player)
            ],
            setup=lambda self:
                player.connect("closed", lambda x: RemoveAddedBox(self))
        )








class MediaPlayer(Widget.Box):
    def __init__(self):
        self.label = Widget.Label(
            label="No Player Is Being Played",
            visible = mpris.bind("players", lambda x: False if len(x) else True),
            valign="center",
            vexpand=True,
            css_classes=["player-availability"]
        )
        mpris.connect("player_added", self.onPlayerAdded)
        super().__init__(
            css_classes=["MediaContainer", "quicksettings-container"],
            vertical=True,
            child=[
                Widget.Label(label="Media",css_classes=["MediaTitle"], halign="start"),
                self.label
            ]
        )
    def onPlayerAdded(self, x, player):
        AddBox(self, Popup(player))
        
        # popup=Popup(player)
        # self.append(popup)
        # popup.revealer.reveal_child=True

