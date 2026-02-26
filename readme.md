# Daily Events Notify version 1.0

This program is a simple program that will notify you of events that are happening today. It will use discord webhook to send the notifications. The program is designed to run on a server and be executed periodically using a cron job or systemd timer.

## Current status

This is minimal viable product. It is able to send notifications to discord based on the events in the json file. You have to manually edit the json file to add or remove events.

In future, if there's many people using this program, we will create a web interface for managing events.

## Setup

**add .env file in the root folder with the following variables**
```
DISCORD_WEBHOOK_URL
TEST_WEBHOOK_URL
```
**then run the following commands**

```bash
cd daily_event_notifier # go to the project root folder
mamba --version # verify that mamba is available in PATH
mamba env create -f environment.yml # create the environment
mamba run -n daily_event_notifier pytest tests/ # run tests
mamba run -n daily_event_notifier python main.py # run the program
```


## To-Do
```
[0] - get more stars on this repo
[1] - create postgresql database for storing events
[2] - create a web interface for managing events
[3] - add custom exception classes
[4] - have fun!
```

## Structure

### Folders

-   Core:
    -   config.py
    -   schemas.py
    -   file_manager.py
    -   event_manager.py
    -   notification_manager.py
    -   main.py

-   Tests:
    -   test_file_manager.py
    -   test_event_manager.py
    -   test_notification_manager.py

-   Data:
    -   events.json # this should be created by the program if not exist

### Data

Base event fields:
```
-   id: str(uuid.uuid4())
-   message: str
-   schedule: "once | daily | weekly | monthly | yearly"
```

Schedule fields:
```
-   date: "datetime": YYYY-MM-DDTHH:MM      (schedule: once)
-   time: "time": HH:MM                     (schedule: daily)
-   day_of_week: "weekday": 0-6             (schedule: weekly)
-   dd: "day": 1-31                         (schedule: monthly)
-   mm_dd: "date": MM-DD                    (schedule: yearly)
```

### Classes

JsonFileManager:
```
-   get_all_data()
-   get_data_by_id(key)
-   add_new_data(value)
-   update_data(key, value)
-   delete_data(key)
```

EventManager:
```
-   get_events()
-   get_todays_events()
-   get_event_by_id(event_id)
-   add_event(event)
-   update_event(event_id, event)
-   delete_event(event_id)
```

NotificationManager:
```
-   send_notification(events)
-   send_error(error)
```
