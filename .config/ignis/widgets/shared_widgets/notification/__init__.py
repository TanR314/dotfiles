from ignis.widgets import Widget
from ignis.utils import Utils
from ignis.services.notifications import NotificationService, Notification

from utils.funcs import AddBox,RemoveAddedBox

notifications = NotificationService.get_default()






class NotificationWidget(Widget.Box):
    def __init__(self, notification: Notification, event="closed", window=False):
        self._event = event
        self._window=window
        self._notification=notification
        # Needed the above three variables for Notification Popups


        self.iconBox = Widget.Icon(
            css_classes=["NotificationIcon"],
            image=notification.icon or "telegram",
            pixel_size=45
        )
        self.summaryBox = Widget.Label(
            css_classes=["NotificationSummary"],
            label=notification.summary,
            halign="start",
            use_markup=True,
            max_width_chars=15,ellipsize='end',
            wrap=True,
            wrap_mode='word_char',
            visible=True if notification.summary else False
        )

        self.bodyBox = Widget.Label(
            css_classes=["NotificationBody"],
            label=notification.body,
            halign="start",
            use_markup=True,
            max_width_chars=15,ellipsize='end',
            wrap=True,
            wrap_mode='word_char',
            visible=True if notification.body else False
        )


        self.actionBox=Widget.Box(
            valign="center",
            css_classes=["NotificationActionBox"],
            child=[
                Widget.Button(
                    # halign="center",
                    child=Widget.Label(label=action.label),
                    on_click=lambda x, action=action: action.invoke(),
                    css_classes=["NotificationAction"],
                )
                for action in notification.actions
            ],
            homogeneous=True,
        )


        self.descriptionBox=Widget.Box(
            css_classes=["NotificationDescriptionBox"],
            vertical=True,
            hexpand=True,
            valign="center",
            child=[
                Widget.Box(
                    hexpand=True,
                    child=[
                        self.summaryBox,
                    ]
                ),
                self.bodyBox,
            ]
        )


        super().__init__(
            css_classes=["NotificationWidget"],
            vertical=True,
            valign="center",
            child=[
                Widget.Box(
                    valign="center",
                    child=[
                        self.iconBox,
                        self.descriptionBox,
                        Widget.Button(
                            css_classes=["NotificationRevealer"],
                            child=Widget.Icon(image="window-close"),
                            on_click=lambda x: notification.close(),
                            valign="start",
                        ),

                    ],
                ),
                self.actionBox
            ],
            setup=lambda self:
                # notification.connect("closed", lambda x: self.unparent())
                notification.connect(self._event,lambda x: self.CloseMe())
        )


    def CloseMe(self):
        # Setup For Notification Popup
        if self._window:
            RemoveAddedBox(self)
            def hideWindow():
                self._window.visible=False

            if len(self._window.MyBox.child) <= 1:
                Utils.Timeout(100, lambda: hideWindow())
        else:
            RemoveAddedBox(self)














