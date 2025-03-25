from ignis.widgets import Widget
# def MyPlayer(player: M):
from gi.repository import Gio

from utils.funcs import Format_Time


class MyPlayer(Widget.Box):
    def __init__(self, player) -> None:



        if player.desktop_entry:
            try:
                if not player.desktop_entry == "spotify":
                    self._app_icon = Gio.DesktopAppInfo.new(player.desktop_entry + ".desktop").get_icon()
                    self.app_icon = self._app_icon.to_string()
                else:
                    self._app_icon = Gio.DesktopAppInfo.new("spotify-launcher" + ".desktop").get_icon()
                    self.app_icon = self._app_icon.to_string()
            except:
                print("OMG")
                # self.app_icon = self._app_icon.to_string()
        else:
            self.app_icon = "telegram"



        self.coverPage = Widget.Box(
            css_classes=["player-coverpage"],
            style=player.bind(
                "art_url",
                lambda x:
                    f'''
                    min-width: 80px;
                    min-height: 80px;
                    background-image: url('file:///{x or "home/jawadhc/Pictures/Wallpapers/your-name-shooting-3840x2160-14938.jpg"}');
                    background-size: cover;
                    background-position: center;
                    '''
            )
        )



        self.descriptionBox = Widget.Box(
            vertical=True,
            hexpand=True,
            vexpand=False,
            valign="start",
            halign="start",
            # style="min-width: 200px;",
            child=[
                Widget.Label(
                    vexpand=False,
                    valign="center",
                    halign="start",
                    label=player.bind("title"),
                    max_width_chars=20,ellipsize='end',
                    wrap_mode='word_char',
                    css_classes=["player-title"]
                ),
                Widget.Label(
                    vexpand=False,
                    valign="center",
                    halign="start",
                    label=player.bind("artist"),
                    max_width_chars=20,ellipsize='end',
                    wrap_mode='word_char',
                    css_classes=["player-artist"]
                )
            ]
        )


        self.slider = Widget.Scale(
            value=player.bind("position", lambda x: x if x != None else 0),
            max=player.bind("length"),
            hexpand=True,
            on_change=lambda x: player.set_position(x.value),
            visible=player.bind(
                "position", lambda value: value != -1
            ),
            css_classes=["slider","player-slider"]
        )


        self.controller = Widget.Box(
            valign="center",
            halign="center",
            # hexpand=False,
            vexpand=False,
            child=[
                Widget.Button(
                    valign="center",
                    child=Widget.Icon(
                        image="media-skip-backward-symbolic",
                        pixel_size=10,
                    ),
                    on_click=lambda x: player.previous(),
                    css_classes = player.bind(
                        "can_go_previous",
                        lambda x:
                            ["player-control-button"]
                            if x
                            else ["player-control-button", "disabled"]
                    )
                ),
                Widget.Button(
                    child=Widget.Icon(
                        valign="center",
                        image=player.bind(
                            "playback_status",
                            lambda x:
                                "media-playback-pause-symbolic" if x=="Playing"
                                else "media-playback-start-symbolic",
                        ),
                        pixel_size=12,
                    ),
                    on_click=lambda x: player.play_pause(),  
                    css_classes=["player-control-button"]
                ),
                Widget.Button(
                    valign="center",
                    child=Widget.Icon(
                        image="media-skip-forward-symbolic",
                        pixel_size=10,
                    ),
                    on_click=lambda x: player.next(),  
                    css_classes = player.bind(
                        "can_go_previous",
                        lambda x:
                            ["player-control-button"]
                            if x
                            else ["player-control-button", "disabled"]
                    )
                ),
            ]
        )

        super().__init__(
            css_classes=["player-container"],
            hexpand=False,
            style="min-width: 310px;",
            child=[
                self.coverPage,
                Widget.Box(
                    vertical=True,
                    hexpand=True,
                    css_classes=["player-info-box"],
                    child=[
                        Widget.Box(
                            child=[
                                self.descriptionBox,
                                Widget.Icon(image=self.app_icon, valign="start", css_classes=["player-app-icon"])
                            ]
                        ),
                        Widget.Box(
                            vertical=True,
                            vexpand=True,
                            valign="end",
                            child=[
                                self.slider,
                                Widget.CenterBox(
                                    start_widget=Widget.Label(
                                        css_classes=["player-time"],
                                        label=player.bind(
                                            "position",
                                            lambda x:
                                                Format_Time(x)
                                        )
                                    ),
                                    center_widget=self.controller,
                                    end_widget=Widget.Label(
                                        css_classes=["player-time"],
                                        label=player.bind(
                                            "length",
                                            lambda x:
                                                Format_Time(x)
                                        )
                                    ),
                                )
                            ]
                        )
                    ]
                )
            ],
        )
