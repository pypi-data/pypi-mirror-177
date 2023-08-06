import subprocess
import getpass
from datetime import datetime, timedelta
import os
import time

from crontab import CronTab


def set_timed_message(date: str = None, hour: str = None, message: str = None):
    """
    date: Date input from user. Expected format is: d/m/Y. Can also be 'today' or 'tomorrow'.
    hour: Hour input from user. Expected format is: H:M.
    message: Message for slackbot to send you when time comes. Any string input is ok.
    """

    try:
        if date.upper() not in ["TODAY", "TOMORROW"]:
            assert len(date.split("/")) == 3
            assert len(date.split("/")[0]) == 2
            assert len(date.split("/")[1]) == 2
            assert len(date.split("/")[2]) == 4
            date = date.split("/")
        else:
            if date.upper() == "TODAY":
                date = str(datetime.now().date()).split("-")[::-1]
            elif date.upper() == "TOMORROW":
                date = str((datetime.now() + timedelta(days=1)).date()).split("-")[::-1]
    except:
        print(
            "ERROR : Wrong date input. Date must be specified in d/m/Y format. (Ex: -d 31/12/2021)"
        )
        return
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
    if message is None:
        print(
            "ERROR : Message is None. Please provide message text. (Ex. -m 'hello world')"
        )
        return

    timezoned_datetime = timezone_converter(
        date, hour, eval(os.getenv("PREF_TIMEZONE"))
    )

    latest_id = list_timed_message(last=True) + 1
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
        command="{0} -m '{1}' -f {2}".format(exec_command, message, latest_id),
        comment="{'PID':" + str(latest_id) + ",'PTP':'T'}",
    )
    job.setall(timezoned_datetime)
    cron.write()

    print("SUCCESS: Timed message is set as")

    list_timed_message(pid=list_timed_message(last=True))

    return


def list_timed_message(pid: int = None, last: bool = False):
    """
    pid: Process ID of the timed message task.
    last: If true, returns latest id of the entries.
    """

    cron = CronTab(user=getpass.getuser())
    jobs = []

    if last:
        latest_id = 0
        for job in cron:
            try:
                if eval(job.comment)["PTP"] != "T":
                    continue
            except:
                continue
            else:
                if eval(job.comment)["PID"] > latest_id:
                    latest_id = eval(job.comment)["PID"]
        return latest_id

    if pid is not None:
        for job in cron.find_comment("{'PID':" + str(pid) + ",'PTP':'T'}"):
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
                if eval(job.comment)["PTP"] != "T":
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


def remove_timed_message(pid: int = None, remove_all=False):
    if remove_all:
        ans = "a"
        while ans not in ["y", "n"]:
            ans = input(
                "WARNING: You are going to remove ALL slackbot-timed messages. Please confirm: [y/n] "
            ).lower()
        if ans == "n":
            print("ABORTED!")
            return False
        else:
            last_id = list_timed_message(last=True)
            cron = CronTab(user=getpass.getuser())
            for i in range(last_id + 1):
                for job in cron.find_comment("{'PID':" + str(i) + ",'PTP':'T'}"):
                    job.delete()
                    cron.write()
            return True

    if pid is not None:
        if not list_timed_message(pid=pid):
            print("ERROR: Given PID: {0} has not found.".format(pid))
            return False
    else:
        print("ERROR: No PID is given")
        return False

    cron = CronTab(user=getpass.getuser())

    for job in cron.find_comment("{'PID':" + str(pid) + ",'PTP':'T'}"):
        job.delete()
    cron.write()

    print("SUCCESS: Process with ID {0} has removed from tasks list.".format(pid))
    return True


def timezone_converter(inpt_date, inpt_hour, pref_offset):
    curr_datetime = datetime(
        int(inpt_date[2]),
        int(inpt_date[1]),
        int(inpt_date[0]),
        int(inpt_hour[0]),
        int(inpt_hour[1]),
    )

    local_offset = time.localtime().tm_gmtoff / (60 * 60)
    diff_offset = local_offset - pref_offset

    if diff_offset > 0:
        new_datetime = curr_datetime + timedelta(hours=abs(diff_offset))
    elif diff_offset < 0:
        new_datetime = curr_datetime - timedelta(hours=abs(diff_offset))
    else:
        return curr_datetime

    return new_datetime
