# Personalized Slack Bot

#### _Version 0.2.3_

-----------
## Installization:
1. Clone the Repository
2. ```pip install <path_to_cloned_dir>/Personalized-Slack-Bot```
3. ```slackbot-config``` For configuring your slackbot token, your user and application settings.

### **The package can be used with 2 different methods. An importable python3 library and as a terminal command.**

## Python Usage:
```import slackbot```

### 1. Editing Configuration:
* **edit_conf()** ---> Allows you to configure Slack credentials and application settings. (Automatically called on the first time run.)

### 2. Sending Instant Messages & Notifications:
* **send_message(message)** ---> Allows you to send a specified message via the bot.
* **start_notif(message = None)** ---> Allows you to send a notification about a task being started.
* **end_notif(message = None)** ---> Allows you to send a notification about a task being finished.

### 3. Sending Not-Recurred Timed Messages:
* **set_timed_message(date, hour, message)** ---> Allows you to set a timed message.
* **list_timed_message(PID = None)** ---> Allows you to list a/all timed messages.
* **remove_timed_message(PID = None, remove_all = False)** ---> Allows you to remove a/all timed messages.

### 4. Sending Recurred Messages:
* **set_reminder(message,hour = None)** ---> Allows you to set a reminder message.
* **list_reminder(PID = None)** ---> Allows you to list your reminder messages.
* **remove_reminder(PID=None, remove_all = False)** ---> Allows you to remove a/all reminder message.

## Terminal Usage:

### 1. Editing Configuration:
* **slackbot-config** ---> Allows you to configure Slack credentials and application settings.


### 2. Sending Instant Messages & Notifications:
* **slackbot-message** ---> Allows you to send a specified message via the bot.
  
  Ex: ```slackbot-message -m 'Hello World, this is an example message!'```
* **slackbot-task_start_notif** ---> Allows you to send a notification about a task being started.
  
  Ex: ```slackbot-task_start_notif```
* **slackbot-task_end_notif** ---> Allows you to send a notification about a task being finished.
  
  Ex: ```slackbot-task_end_notif -m 'Main_Task'```

### 3. Sending Not-Recurred Timed Messages:
* **slackbot-set_timed_message** ---> Allows you to set a timed message.

  Ex: ```slackbot-set_timed_message -d '12/12/2020' -t '18:30' -m 'Did you miss me?'```
* **slackbot-list_timed_message** ---> Allows you to list a/all timed messages.
  
    Ex: ```slackbot-list_timed_message``` _Lists all tasks_
      
    **-or-**
      
    Ex: ```slackbot-list_timed_message -p 5``` _Lists the task with PID = 5_
* **slackbot-remove_timed_message** ---> Allows you to remove a/all timed messages.
  
    Ex: ```slackbot-remove_timed_message -p 2``` _Removes the task with PID = 2_

    **- or -**

    Ex: ```slackbot-remove_timed_message -r``` _Wipes out all timed messages._

### 4. Sending Recurred Messages:
* **slackbot-set_reminder** ---> Allows you to set a reminder message.
  
    Ex: ```slackbot-set_reminder -m 'Don't forget to remember what you always forget.```
* **slackbot-list_reminder** ---> Allows you to list your reminder messages.
  
    Ex: ```slackbot-list_reminder```
* **slackbot-remove_reminder** ---> Allows you to remove a reminder message.

    Ex: ```slackbot-remove_reminder -r```
    
    Ex: ```slackbot-remove_reminder -p 6```

  
