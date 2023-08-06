import subprocess
import getpass
import os
import time

from crontab import CronTab


def set_reminder(message: str = None, hour: str = None):
    """
    hour (optional): Hour input from user. Expected format is: H:M.
    message: Message for slackbot to send you when time comes. Any string input is ok.
    """
    if hour is not None:
        try:
            assert len(hour.split(":")) == 2
            assert len(hour.split(":")[0]) == 2
            assert len(hour.split(":")[1]) == 2
            hour = hour.split(":")
        except:
            print(
                "ERROR : Wrong hour input. Hour must be specified in H:M format. (Ex: -t 14:59)"
            )
            return
    else:
        hour = os.getenv("REMINDER_TIME").split(":")
    if message is None:
        print(
            "ERROR : Message is None. Please provide message text. (Ex. -m 'hello world')"
        )
        return

    timezoned_hour = reminder_timezone_converter(hour, eval(os.getenv("PREF_TIMEZONE")))

    latest_id = list_reminder_message(last=True) + 1

    exec_command = ""
    if os.getenv("SLACKBOT_PATH") not in ["-", "", None, "None"]:
        exec_command = os.getenv("SLACKBOT_PATH") + "-message"

    elif os.getenv("USED-SHELL") not in ["-", "", None, "None"]:
        exec_command = (
            subprocess.run(
                "where slackbot-message",
                shell=True,
                executable=os.getenv("USED-SHELL"),
                capture_output=True,
            )
            .stdout.decode("utf-8")
            .replace("\n", "")
        )
    else:
        for env in ["bin/zsh", "bin/bash"]:
            try:
                exec_command = (
                    subprocess.run(
                        "where slackbot-message",
                        shell=True,
                        executable=env,
                        capture_output=True,
                    )
                    .stdout.decode("utf-8")
                    .replace("\n", "")
                )
            except:
                continue
            if len(exec_command) > 1:
                break

    if len(exec_command) == 0:
        print("ERROR : Executeable slackbot path is not found.")
        print(
            "Please provide your shell env that slackbot installed or provide slackbot location by calling slackbot-config."
        )
        return

    cron = CronTab(getpass.getuser())
    job = cron.new(
        command="{0} -m '{1}'".format(exec_command, message),
        comment="{'PID':" + str(latest_id) + ",'PTP':'R'}",
    )
    job.hour.on(timezoned_hour[0]), job.minute.on(timezoned_hour[1])
    cron.write()

    print("SUCCESS: Reminder message is set as")

    list_reminder_message(pid=list_reminder_message(last=True))

    return


def list_reminder_message(pid: int = None, last: bool = False):
    """
    pid: Process ID of the reminder message task.
    last: If true, returns latest id of the entries.
    """

    cron = CronTab(user=getpass.getuser())
    jobs = []

    if last:
        latest_id = 0
        for job in cron:
            try:
                if eval(job.comment)["PTP"] != "R":
                    continue
            except:
                continue
            else:
                if eval(job.comment)["PID"] > latest_id:
                    latest_id = eval(job.comment)["PID"]
        return latest_id

    if pid is not None:
        for job in cron.find_comment("{'PID':" + str(pid) + ",'PTP':'R'}"):
            cron = ""
            for p in job.slices:
                cron += str(p) + " "
            job_info = {
                **eval(job.comment),
                **{
                    "MESSAGE": job.command.split("-m")[-1:][0]
                    .replace("'", "")
                    .strip()
                    .split("-f")[0]
                },
                **{"CRON": cron.strip()},
            }
            jobs.append(job_info)

    else:
        for job in cron:
            try:
                if eval(job.comment)["PTP"] != "R":
                    continue
            except:
                continue
            cron = ""
            for p in job.slices:
                cron += str(p) + " "
            job_info = {
                **eval(job.comment),
                **{
                    "MESSAGE": job.command.split("-m")[-1:][0]
                    .replace("'", "")
                    .strip()
                    .split("-f")[0]
                },
                **{"CRON": cron.strip()},
            }
            jobs.append(job_info)

    for j in jobs:
        print(j)
    if len(jobs) > 0:
        return True
    else:
        return False


def remove_reminder_message(pid: int = None, remove_all=False):
    if remove_all:
        ans = "a"
        while ans not in ["y", "n"]:
            ans = input(
                "WARNING: You are going to remove ALL slackbot-reminder messages. Please confirm: [y/n] "
            ).lower()
        if ans == "n":
            print("ABORTED!")
            return False
        else:
            last_id = list_reminder_message(last=True)
            cron = CronTab(user=getpass.getuser())
            for i in range(last_id + 1):
                for job in cron.find_comment("{'PID':" + str(i) + ",'PTP':'R'}"):
                    job.delete()
                    cron.write()
            return True

    if pid is not None:
        if not list_reminder_message(pid=pid):
            print("ERROR: Given PID: {0} has not found.".format(pid))
            return False
    else:
        print("ERROR: No PID is given")
        return False

    cron = CronTab(user=getpass.getuser())

    for job in cron.find_comment("{'PID':" + str(pid) + ",'PTP':'R'}"):
        job.delete()
    cron.write()

    print("SUCCESS: Process with ID {0} has removed from tasks list.".format(pid))
    return True


def reminder_timezone_converter(inpt_hour, pref_offset):
    local_offset = time.localtime().tm_gmtoff / (60 * 60)
    diff_offset = local_offset - pref_offset

    hour = int(inpt_hour[0]) + diff_offset

    if hour < 0:
        hour += 24
    elif hour > 23:
        hour -= 24

    return [int(hour), int(inpt_hour[1])]
