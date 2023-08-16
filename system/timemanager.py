from datetime import datetime

import pytz

import main


class Timemanager():
    def __init__(self):
        self.timezone = pytz.timezone(main.bot_time_zone)

    def get_time(self):
        return datetime.now(self.timezone)
    def format_time(self,time):
        #only hours and minutes
        return time.strftime("%H:%M")
    def format_seconds(self,seconds):
        time = seconds
        timesuffix = "S"
        if seconds >= 60:
            time = seconds / 60
            timesuffix = "M"
            if time >= 60:
                time = time / 60
                timesuffix = "H"
                if time >= 24:
                    time = time / 24
                    timesuffix = "D"
                    if time >= 365:
                        time = time / 365
                        timesuffix = "Y"
        return str(round(time,2)) + timesuffix
    def get_time_difference(self,first,second):
        return (first - second).total_seconds()
    def get_bot_uptime(self):
        botrunseconds = main.run_time
        return self.format_seconds(botrunseconds)
    def get_but_uptime_raw(self):
        return main.run_time


