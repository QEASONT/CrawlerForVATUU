import datetime, os
# from msilib.schema import tables
from icalendar import Calendar, Event
import re
import json
import uuid


class Event:
    """
    事件对象
    """

    def __init__(self, kwargs):
        self.event_data = kwargs

    def __turn_to_string__(self):
        self.event_text = "BEGIN:VEVENT\n"
        for item, data in self.event_data.items():
            item = str(item).replace("_", "-")
            if item not in ["ORGANIZER", "DTSTART", "DTEND"]:
                self.event_text += "%s:%s\n" % (item, data)
            else:
                self.event_text += "%s;%s\n" % (item, data)
        self.event_text += '''BEGIN:VALARM\nTRIGGER:-PT15M\nSUMMARY:闹钟\nACTION:DISPLAY\nDESCRIPTION:还有15分钟上课哦！\nEND:VALARM\n'''
        self.event_text += "END:VEVENT\n"
        return self.event_text


class Calendar:
    """
    日历对象
    """

    def __init__(self, calendar_name="My Calendar"):
        self.__events__ = {}
        self.__event_id__ = 0
        self.calendar_name = calendar_name

    def add_event(self, **kwargs):
        event = Event(kwargs)
        event_id = self.__event_id__
        self.__events__[self.__event_id__] = event
        self.__event_id__ += 1
        return event_id

    def modify_event(self, event_id, **kwargs):
        for item, data in kwargs.items():
            self.__events__[event_id].event_data[item] = data

    def remove_event(self, event_id):
        self.__events__.pop(event_id)

    def get_ics_text(self):
        self.__calendar_text__ = """BEGIN:VCALENDAR\nPRODID:-//ZHONG_BAI_REN//APPGENIX-SOFTWARE//\nVERSION:2.0\nCALSCALE:GREGORIAN\nMETHOD:PUBLISH\nX-WR-CALNAME:%s\nX-WR-TIMEZONE:null\n""" % self.calendar_name
        for key, value in self.__events__.items():
            self.__calendar_text__ += value.__turn_to_string__()
        self.__calendar_text__ += "END:VCALENDAR"
        return self.__calendar_text__

    def save_as_ics_file(self):
        ics_text = self.get_ics_text()
        open("%s.ics" % self.calendar_name, "w",
             encoding="utf8").write(ics_text)  #使用utf8编码生成ics文件，否则日历软件打开是乱码

    def open_ics_file(self):
        os.system("%s.ics" % self.calendar_name)


def add_event(cal, SUMMARY, DTSTART, DTEND, DESCRIPTION, LOCATION):
    """
    向Calendar日历对象添加事件的方法
    :param cal: calender日历实例
    :param SUMMARY: 事件名
    :param DTSTART: 事件开始时间
    :param DTEND: 时间结束时间
    :param DESCRIPTION: 备注
    :param LOCATION: 时间地点
    :return:
    """
    time_format = "TZID=Asia/Shanghai:{date.year}{date.month:0>2d}{date.day:0>2d}T{date.hour:0>2d}{date.minute:0>2d}00"
    # DALARM = DTSTART-datetime.timedelta(minutes=15)
    # dt_alarm = time_format.format(date=DALARM)
    dt_start = time_format.format(date=DTSTART)
    dt_end = time_format.format(date=DTEND)
    create_time = datetime.datetime.today().strftime("%Y%m%dT%H%M%SZ")
    uid = str(uuid.uuid4())
    suid = ''.join(uid.split('-'))
    cal.add_event(
        SUMMARY=SUMMARY,
        ORGANIZER="CN=My Calendar:mailto:1852771880@qq.com",
        DTSTART=dt_start,
        #   DTALARM = dt_alarm,
        DTEND=dt_end,
        DTSTAMP=create_time,
        UID="{}{}-11@1852771880@qq.com".format(create_time, suid),
        SEQUENCE="0",
        CREATED=create_time,
        DESCRIPTION=DESCRIPTION,
        LAST_MODIFIED=create_time,
        LOCATION=LOCATION,
        STATUS="CONFIRMED",
        TRANSP="OPAQUE")


def generateSchedule(cal, table):

    for col in range(2, len(table[0])):
        hashTable = [1] * 14
        for row in range(1, len(table)):
            if hashTable[row]:
                if table[row][col][0] == ' ':
                    continue
                startTimeRow = row
                while row != len(table) - 1:
                    if table[row + 1][col][0][0:5] != table[row][col][0][0:5]:
                        break
                    else:
                        row += 1
                endTimeRow = row
                for i in range(startTimeRow, min(endTimeRow + 1, len(table))):
                    hashTable[i] = 0
                name = table[startTimeRow][col][0]
                nameList = re.split('  | |\n', name)
                startTime = table[startTimeRow][1][0]
                endTime = table[endTimeRow][1][0]
                startTimeList = re.split(':|-', startTime)
                endTimeList = re.split(':|-', endTime)
                date = table[0][col][0]
                dateList = re.split('\n|月|日', date)
                print(nameList[0])
                print(startTime)
                print(endTime)
                # if nameList[3][-1] == '）':
                #     summary = (nameList[0] + ' ' + nameList[1] + ' ' +
                #                nameList[2] + ' ' + nameList[3])
                #     description = nameList[4]
                #     location = nameList[5]
                # else:
                #     summary = (nameList[0] + ' ' + nameList[1] + ' ' +
                #                nameList[2])
                #     description = nameList[3]
                #     location = nameList[4]
                if nameList[3][-1] == '）':
                    summary = (nameList[0] + ' ' + nameList[1] + ' ' +
                               nameList[2] + ' ' + nameList[3])
                    description = nameList[4]
                    location = nameList[5]
                else:
                    if len(nameList) == 4:

                        summary = (nameList[0] + ' ' + nameList[1] + ' ' +
                                   nameList[2])
                        description = nameList[2]
                        location = nameList[3]
                    else:
                        if "（null）" in nameList[2]:
                            nameList[2] = nameList[2].split("（null）")[0]
                        summary = (nameList[0] + ' ' + nameList[1] + ' ' +
                                   nameList[2])
                        description = nameList[3]
                        location = nameList[4]
                add_event(cal,
                          SUMMARY=summary,
                          DTSTART=datetime.datetime(year=2022,
                                                    month=int(dateList[1]),
                                                    day=int(dateList[2]),
                                                    hour=int(startTimeList[0]),
                                                    minute=int(
                                                        startTimeList[1]),
                                                    second=00),
                          DTEND=datetime.datetime(year=2022,
                                                  month=int(dateList[1]),
                                                  day=int(dateList[2]),
                                                  hour=int(endTimeList[2]),
                                                  minute=int(endTimeList[3]),
                                                  second=00),
                          DESCRIPTION=description,
                          LOCATION=location)
    return cal


if __name__ == '__main__':
    with open('table.json', mode='r', encoding='utf-8') as f:
        totaltable = json.load(f)
    cal = Calendar(calendar_name="22-23 SWJTU-Leeds")
    for table in totaltable:
        calendar = generateSchedule(cal, table)
    calendar.save_as_ics_file()