#!/usr/bin/env python

import datetime
from datetime import date, datetime
from adhan import adhan
from adhan.methods import ISNA, ASR_STANDARD
from typing import Set, Tuple, Dict, List

PrayerDict = Dict[str, datetime]


class Adhans:
    def __init__(
        self,
        methodology: Dict,
        asr: Dict,
        lattitude: float,
        longitude: float,
        timezone_offset: int,
    ) -> None:
        self.timezone_offset: int = timezone_offset
        self.latti_longi_tuple: Tuple = (lattitude, longitude)
        self.params: Dict = {}
        self.params.update(methodology)
        self.params.update(asr)
        self.adhan_times: PrayerDict = self.get_adhan_times()

    def get_adhan_times(self) -> PrayerDict:
        adhan_times: PrayerDict = adhan(
            day=date.today(),
            location=self.latti_longi_tuple,
            parameters=self.params,
            timezone_offset=self.timezone_offset,
        )
        return adhan_times

    def get_closest_prayer(self) -> Tuple[str, datetime]:
        prayer_times: List[datetime] = [
            self.adhan_times[x] for x in self.adhan_times.keys()
        ]
        closest_prayer_time: datetime = min(
            [i for i in prayer_times if i <= datetime.now()],
            key=lambda x: abs(
                x - datetime.now(),
            ),
        )
        closest_prayer: Set[str] = {
            i for i in self.adhan_times if self.adhan_times[i] == closest_prayer_time
        }

        match str(closest_prayer).replace("{", "").replace("}", "").replace("'", ""):
            case "fajr":
                return_var = (" Fajr", self.adhan_times["fajr"])
            case "shuruq":
                return_var = (" Duhaa", self.adhan_times["shuruq"])
            case "zuhr":
                return_var = (" Dhuhr", self.adhan_times["zuhr"])
            case "asr":
                return_var = (" Asr", self.adhan_times["asr"])
            case "maghrib":
                return_var = (" Maghrib", self.adhan_times["maghrib"])
            case "isha":
                return_var = (" Isha", self.adhan_times["isha"])
            case _:
                return_var = ("????", datetime.now())
        return return_var


def start():
    adhans = Adhans(ISNA, ASR_STANDARD, 33.6595, 117.9988, -8)
    adhans.get_closest_prayer()


if __name__ == "__main__":
    start()
