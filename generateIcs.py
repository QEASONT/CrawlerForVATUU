import ics
import json
from pandas import DataFrame
import pandas

calendar = ics.Calendar(calendar_name="22-23 SWJTU-Leeds")
excel_writer = pandas.ExcelWriter('schedule.xlsx')  # 定义writer，选择文件（文件可以不存在）
with open('table.json', mode='r', encoding='utf-8') as f:
    totalTable = json.load(f)

for table in totalTable:
    ics.generateSchedule(calendar, table)
calendar.save_as_ics_file()