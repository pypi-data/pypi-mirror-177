from setuptools import setup, find_packages

__version__ = "0.2.3"

setup(
    name="personalized-slack-bot",
    version=__version__,
    license="MIT",
    author="Eren Ali Aslangiray",
    entry_points={
        "console_scripts": [
            "slackbot = terminal_wrapper.wrapper:help",
            "slackbot-config = slackbot.config:edit_conf",
            "slackbot-message = terminal_wrapper.wrapper:message_wrapper",
            "slackbot-task_start_notif = terminal_wrapper.wrapper:start_notif_wrapper",
            "slackbot-task_end_notif = terminal_wrapper.wrapper:end_notif_wrapper",
            "slackbot-set_timed_message = terminal_wrapper.wrapper:set_timed_message_wrapper",
            "slackbot-list_timed_message = terminal_wrapper.wrapper:list_timed_message_wrapper",
            "slackbot-remove_timed_message = terminal_wrapper.wrapper:remove_timed_message_wrapper",
            "slackbot-set_reminder = terminal_wrapper.wrapper:set_reminder_message_wrapper",
            "slackbot-list_reminder = terminal_wrapper.wrapper:list_reminder_message_wrapper",
            "slackbot-remove_reminder = terminal_wrapper.wrapper:remove_reminder_message_wrapper",
        ]
    },
    packages=find_packages("src"),
    package_dir={"":"src"},
    url = "https://github.com/Erenaliaslangiray/Personalized-Slack-Bot",
    install_requires=['setuptools ==57.4.0', 'slack-sdk == 3.1.0', 'python-dotenv == 0.19.0', 'python-crontab == 2.5.1'],
)
