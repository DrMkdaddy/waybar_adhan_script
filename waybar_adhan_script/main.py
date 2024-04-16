#!/usr/bin/env python

import datetime
from datetime import date, datetime
from adhan import adhan
from adhan.methods import ISNA, ASR_STANDARD

PrayerDict = dict[str, datetime]


class Adhans:
    def __init__(
        self,
        methodology: dict,
        asr: dict,
        lattitude: float,
        longitude: float,
        timezone_offset: int,
    ):
        self.timezone_offset: int = timezone_offset
        self.latti_longi_tuple: tuple = (lattitude, longitude)
        self.params: dict = {}
        self.params.update(methodology)
        self.params.update(asr)
        self.adhan_times: PrayerDict = self.get_adhan_times()

    def get_adhan_times(self):
        adhan_times: PrayerDict = adhan(
            day=date.today(),
            location=self.latti_longi_tuple,
            parameters=self.params,
            timezone_offset=self.timezone_offset,
        )
        return adhan_times

    def get_closest_prayer(self):
        prayer_times: list[datetime] = [
            self.adhan_times[x] for x in self.adhan_times.keys()
        ]
        closest_prayer_time: datetime = min(
            [i for i in prayer_times if i <= datetime.now()],
            key=lambda x: abs(
                x - datetime.now(),
            ),
        )
        closest_prayer: set[str] = {
            i for i in self.adhan_times if self.adhan_times[i] == closest_prayer_time
        }

        match str(closest_prayer):
            case "{'fajr'}":
                print(" Fajr")
            case "{'shuruq'}":
                print(" Duhaa")
            case "{'zhur'}":
                print(" Dhuhr")
            case "{'asr'}":
                print(" Asr")
            case "{'maghrib'}":
                print(" Maghrib")
            case "{'isha'}":
                print(" Isha")
            case _:
                print("????")


if __name__ == "__main__":
    adhans = Adhans(ISNA, ASR_STANDARD, 33.6595, 117.9988, -8)
    adhans.get_closest_prayer()
