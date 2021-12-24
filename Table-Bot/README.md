# TimetableBot

Written in Python using PostgreSQL and telebot:
```python
import telebot
from telebot import types
import psycopg2
from datetime import datetime, date
```
A telegram bot on Python that sends the BFI2102 schedule. The program automatically determines the type of the current week using the "datetime" library.
####
The bot supports the following commands:
- "Monday", "Tuesday", "Wednesday", "Thursday", "Friday" - sends the schedule for the specified day.
- "Schedule for the current week" - sends the schedule for the current week.
- "Schedule for the next week" - sends the schedule for the next week.
- /week - specifies the type of the current week.
- /help - sends a list of bot commands.
- /mtuci - sends a link to the official MTUCI website.
