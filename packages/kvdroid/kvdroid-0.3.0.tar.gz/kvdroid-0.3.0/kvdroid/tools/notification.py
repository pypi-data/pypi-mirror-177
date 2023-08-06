from typing import Union
from jnius import cast, JavaException  # NOQA
from android import python_act  # NOQA
from kvdroid import Logger, activity
from kvdroid.cast import cast_object
from kvdroid.jclass.android import BitmapFactory
from kvdroid.jclass.java import InputStream
from kvdroid.tools import get_resource
from kvdroid.tools.graphics import bitmap_to_drawable

BitmapFactory = BitmapFactory()

try:
    from kvdroid.jclass.androidx import (
        ContextCompat,
        NotificationCompatBuilder,
        NotificationCompat,
        NotificationCompatActionBuilder,
        RemoteInputBuilder,
        NotificationCompatBigPictureStyle,
        NotificationBigTextStyle
    )
    from kvdroid.jclass.android import (
        Intent,
        Context,
        PendingIntent,
        NotificationManager,
        Notification,
        VERSION
    )
    from kvdroid.jclass.java.lang import String, System


    def create_notification(
            small_icon: Union[int, str, InputStream()], channel_id: str, title: str,
            text: str, ids: int, channel_name: str,
            large_icon: Union[int, str, InputStream()] = 0, big_picture: Union[int, str, InputStream()] = 0,
            action_title1: str = "", action_title2: str = "", action_title3: str = "", key_text_reply: str = "",
            reply_title: str = "",
            expandable: bool = False, set_large_icon: bool = False, add_action_button2: bool = False,
            add_action_button3: bool = False, auto_cancel: bool = True, add_action_button1: bool = False,
            set_reply: bool = False, put_extra: bool = False, extras: tuple = ("test", "test"),
            small_icon_color: int = 0
    ):  # sourcery no-metrics
        intent = Intent(activity.getApplication().getApplicationContext(), python_act)
        if put_extra:
            intent.putExtra(*extras)
        intent.setFlags(Intent().FLAG_ACTIVITY_CLEAR_TOP | Intent().FLAG_ACTIVITY_SINGLE_TOP)
        intent.setAction(Intent().ACTION_MAIN)
        intent.addCategory(Intent().CATEGORY_LAUNCHER)
        if VERSION().SDK_INT >= 31:
            pendingIntent = PendingIntent().getActivity(
                activity.getApplication().getApplicationContext(), 0, intent,
                PendingIntent().FLAG_MUTABLE
            )
        else:
            pendingIntent = PendingIntent().getActivity(
                activity.getApplication().getApplicationContext(), 0, intent,
                PendingIntent().FLAG_UPDATE_CURRENT | Notification().FLAG_AUTO_CANCEL
            )
        # Create the NotificationChannel, but only on API 26+ because
        # the NotificationChannel class is new and not in the support library
        notificationManager = cast(NotificationManager(), activity.getSystemService(
            Context().NOTIFICATION_SERVICE
        ))
        if VERSION().SDK_INT >= 26:
            from kvdroid.jclass.android.app import NotificationChannel
            importance: int = NotificationManager().IMPORTANCE_HIGH
            channel = NotificationChannel(String(channel_id), String(channel_name), importance)
            channel.setDescription("notification")
            # Register the channel with the system; you can't change the importance
            # or other notification behaviors after this
            notificationManager.createNotificationChannel(channel)

        builder = NotificationCompatBuilder(activity.getApplication().getApplicationContext(), channel_id)
        if isinstance(small_icon, int):
            builder.setSmallIcon(small_icon)
        else:
            builder.setSmallIcon(bitmap_to_drawable(small_icon))
        if small_icon_color:
            try:
                builder.setColor(ContextCompat().getColor(activity.getApplicationContext(), small_icon_color))
            except JavaException:
                builder.setColor(small_icon_color)
        builder.setContentTitle(String(title))
        builder.setContentText(String(text))
        # Set the intent that will fire when the user taps the notification
        builder.setContentIntent(pendingIntent)
        builder.setWhen(System().currentTimeMillis())
        builder.setChannelId(String(channel_id))
        builder.setPriority(NotificationCompat().PRIORITY_HIGH)
        builder.setDefaults(NotificationCompat().DEFAULT_ALL)
        builder.setAutoCancel(auto_cancel)
        builder.setTicker(String(""))
        builder.setContentInfo("INFO")
        builder.setStyle(NotificationBigTextStyle(instantiate=True).bigText(String(text)).setBigContentTitle(text))
        if add_action_button1:
            builder.addAction(
                get_resource("mipmap").icon, cast_object("charSequence", String(action_title1)), pendingIntent
            )

        if add_action_button2:
            builder.addAction(
                get_resource("mipmap").icon, cast_object("charSequence", String(action_title2)), pendingIntent
            )

        if add_action_button3:
            builder.addAction(
                get_resource("mipmap").icon, cast_object("charSequence", String(action_title3)), pendingIntent
            )

        if set_reply:
            builder.addAction(
                NotificationCompatActionBuilder(
                    get_resource("mipmap").icon, String(reply_title), pendingIntent).addRemoteInput(
                    RemoteInputBuilder(String(key_text_reply)).setLabel(
                        String(reply_title)).build()
                ).build()
            ).setAutoCancel(auto_cancel)

        if expandable:
            largePicture = NotificationCompatBigPictureStyle(instantiate=True)
            if isinstance(big_picture, int):
                largePicture.bigPicture(BitmapFactory.decodeResource(activity.getResources(), big_picture))
            elif isinstance(big_picture, str):
                largePicture.bigPicture(BitmapFactory.decodeFile(big_picture))
            else:
                largePicture.bigPicture(BitmapFactory.decodeStream(big_picture))
            builder.setStyle(largePicture)

        if set_large_icon:
            if isinstance(large_icon, int):
                builder.setLargeIcon(BitmapFactory.decodeResource(activity.getResources(), large_icon))
            elif isinstance(large_icon, str):
                builder.setLargeIcon(BitmapFactory.decodeFile(large_icon))
            else:
                builder.setLargeIcon(BitmapFactory.decodeStream(large_icon))

        # notificationId is a unique int for each notification that you must define
        notificationManager.notify(ids, builder.build())
except JavaException as error:
    Logger.error(
        f"{str(error)}\n"
        "Kvdroid: Androidx not Enabled, Cannot Import create_notification\n"
        "Use official kivy plyer module instead or enable androidx in buildozer.spec file"
    )
