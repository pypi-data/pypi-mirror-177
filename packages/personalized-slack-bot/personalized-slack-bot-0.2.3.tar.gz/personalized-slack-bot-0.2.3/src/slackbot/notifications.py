from .message import send_message


def start_notif(message=None):
    if message is None:
        send_message("Process is started! 🏎 💨")
    else:
        send_message("Process with name: {} is started! 🏎 💨".format(message))


def end_notif(message=None):
    if message is None:
        send_message("Process is finished! 🏁 ✅")
    else:
        send_message("Process with name: {} is finished! 🏁 ✅".format(message))
