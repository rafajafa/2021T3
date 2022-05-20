from timetable import timetable
from datetime import date, time, datetime

def test_timetable_1():
    assert(timetable([date(2019,9,27), date(2019,9,30)], [time(14,10), time(10,30)]) \
        == [datetime(2019, 9, 27, 10, 30), datetime(2019, 9, 27, 14, 10), datetime(2019, 9, 30, 10, 30), datetime(2019, 9, 30, 14, 10)])

def test_timetable_2():
    assert(timetable([date(2021,10,7)], [time(13,35)]) == [datetime(2021, 10, 7, 13, 35)])

def test_timetable_3():
    assert(timetable([date(2021,9,27), date(2021,9,30)], [time(13,56), time(10,30)]) \
        == [datetime(2021, 9, 27, 10, 30), datetime(2021, 9, 27, 13, 56), datetime(2021, 9, 30, 10, 30), datetime(2021, 9, 30, 13, 56)])