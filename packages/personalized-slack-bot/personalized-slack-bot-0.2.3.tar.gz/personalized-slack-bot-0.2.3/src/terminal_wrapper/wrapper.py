from . import options
from slackbot import message, timed_message, reminder_message


def help():
    print(
        "______                               _ _             _   _____ _            _     ______       _   "
    )
    print(
        "| ___ \                             | (_)           | | /  ___| |          | |    | ___ \     | |  "
    )
    print(
        "| |_/ /__ _ __ ___  ___  _ __   __ _| |_ _______  __| | \ `--.| | __ _  ___| | __ | |_/ / ___ | |_ "
    )
    print(
        "|  __/ _ \ '__/ __|/ _ \| '_ \ / _` | | |_  / _ \/ _` |  `--. \ |/ _` |/ __| |/ / | ___ \/ _ \| __|"
    )
    print(
        "| | |  __/ |  \__ \ (_) | | | | (_| | | |/ /  __/ (_| | /\__/ / | (_| | (__|   <  | |_/ / (_) | |_ "
    )
    print(
        "\_|  \___|_|  |___/\___/|_| |_|\__,_|_|_/___\___|\__,_| \____/|_|\__,_|\___|_|\_\ \____/ \___/ \__|"
    )
    print(
        "                                                                                                   "
    )
    print(
        "                                                                                                   "
    )
    print("Available Options:")
    print(
        "slackbot-config ---> Allows you to configure Slack credentials and application settings."
    )
    print("slackbot-message ---> Allows you to send specified message via bot.")
    print(
        "slackbot-task_start_notif ---> Allows you to send a notification about a task being started."
    )
    print(
        "slackbot-task_end_notif ---> Allows you to send a notification about a task being finished."
    )
    print("slackbot-set_timed_message ---> Allows you to set a timed message.")
    print("slackbot-list_timed_message ---> Allows you to list timed messages.")
    print("slackbot-remove_timed_message ---> Allows you to remove a timed message.")
    print("slackbot-set_reminder ---> Allows you to set a reminder message.")
    print("slackbot-list_reminder ---> Allows you to list your reminder messages.")
    print("slackbot-remove_reminder ---> Allows you to remove a reminder message.")
    print("")


def message_wrapper():
    message.send_message(options["MES"], options["FRT"])


def start_notif_wrapper():
    if options["MES"] is None:
        message.send_message("Process is started! 🏎 💨")
    else:
        message.send_message(
            "Process with name: {} is started! 🏎 💨".format(options["MES"])
        )


def end_notif_wrapper():
    if options["MES"] is None:
        message.send_message("Process is finished! 🏁 ✅")
    else:
        message.send_message(
            "Process with name: {} is finished! 🏁 ✅".format(options["MES"])
        )


def set_timed_message_wrapper():
    timed_message.set_timed_message(
        date=options["DAT"], hour=options["TME"], message=options["MES"]
    )


def list_timed_message_wrapper():
    if options["PID"] is None:
        timed_message.list_timed_message()
    else:
        timed_message.list_timed_message(pid=options["PID"])


def remove_timed_message_wrapper():
    if options["PID"] is None:
        timed_message.remove_timed_message(remove_all=options["RMA"])
    else:
        timed_message.remove_timed_message(pid=options["PID"])


def set_reminder_message_wrapper():
    reminder_message.set_reminder(message=options["MES"], hour=options["TME"])


def list_reminder_message_wrapper():
    if options["PID"] is None:
        reminder_message.list_reminder_message()
    else:
        reminder_message.list_reminder_message(pid=options["PID"])


def remove_reminder_message_wrapper():
    if options["PID"] is None:
        reminder_message.remove_reminder_message(remove_all=options["RMA"])
    else:
        reminder_message.remove_reminder_message(pid=options["PID"])
