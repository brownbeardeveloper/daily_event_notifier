# Daily Events Notify

This program is a simple program that will notify you of events that are happening today. It will use slack webhook to send the notifications. The program is designed to run on a server and be executed periodically using a cron job or systemd timer.

## Setup

```bash
mamba --version # verify that mamba is available in PATH
mamba env create -f environment.yml # create the environment
mamba run -n daily_events_notify mycommand # run any command in the environment
```

## To run tests (from root folder)

```bash
mamba run -n daily_events_notify pytest tests/
```

## Development 

This project is developed using test driven development.


## Current status

Early development.


### To-Do
```
[completed] - fix file manager class
[completed] - fix notify manager class
[completed] - fix event manager class
[completed] -  create events.json if not exist
[5] -
[6] -
[7] -
[8] -
[9] -
```

## Structure

### Folders

-   Core:

    -   config.py
    -   schemas.py
    -   file_manager.py
    -   event_manager.py
    -   notify_manager.py
    -   main.py

-   Tests:
    -   test_file_manager.py
    -   test_event_manager.py
    -   test_notify_manager.py

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
-   once: "datetime": YYYY-MM-DDTHH:MM
-   daily: "time": HH:MM
-   weekly: "weekday": 0-6
-   monthly: "day": 1-31
-   yearly: "date": MM-DD
```

### Classes

File_Manager:
```
-   read_json(file_path)
-   write_json(file_path, data)
```

Event_Manager:
```
-   get_events()
-   get_event_by_id(event_id)
-   add_event(event)
-   update_event(event_id, event)
-   delete_event(event_id)
```

Notify_Manager:
```
-   send_notification(events)
-   send_error(error)
```
