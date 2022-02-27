
import imp
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from readtable import text_get_table_row_cell
import time
import xlwt
import json
import re
from PIL import Image
from aip import AipOcr
import pandas
import certify
import ics
from pandas import DataFrame
import openpyxl

import os

def search(driver,isdebug):
    try:#浏览器打开网页
        driver.get("http://jwc.swjtu.edu.cn/index.html?version=2020")#-------------------网址修改之一
        driver.find_element_by_xpath("//*[@id='nav_dl']/dd[3]/a").click()
    except Exception as e:#如果网页打开有误，则直接退出
        print('0'+str(Exception)+' '+str(e)+' '+repr(e)+' '+e.message)
        return 
    # usernameInput = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[2]/form/div/div[1]/input")#.encode('utf-8')
    
    handles = (driver.window_handles)
    driver.switch_to.window(handles[1])
    print((handles))
    while 1:
        start = time.time()
        try:
            usernameInput = driver.find_element_by_xpath('//*[@id="username"]')
            print('已定位到元素')
            end=time.time()
            break
        except:
            print("还未定位到元素!")
        
    usernameInput.click()  
    usernameInput.clear()#.encode('utf-8')  
    usernameInput.send_keys("2019110035")#.encode('utf-8')  

    while 1:
        start = time.time()
        try:
            codeInput = driver.find_element_by_xpath('//*[@id="password"]')
            print('已定位到元素')
            end=time.time()
            break
        except:
            print("还未定位到元素!")
        
    codeInput.click()  
    codeInput.clear()#.encode('utf-8')  
    codeInput.send_keys("qiantang2001007")#.encode('utf-8')  
    
    #验证码识别
    png = driver.find_element_by_xpath('//*[@id="randomPhoto"]/img')  # 查找验证码元素
    png.screenshot('capt.png')  # 对验证码进行截图并保存

    img = Image.open('capt.png')
    img = img.convert('L')  # P模式转换为L模式(灰度模式默认阈值127)
    count = 165  # 设定阈值
    table = []
    for i in range(256):
        if i < count:
            table.append(0)
        else:
            table.append(1)

    img = img.point(table, '1')
    img.save('captcha1.png')  # 保存处理后的验证码

    # 识别码
    APP_ID = '24856778'
    API_KEY = 'WSrIN3ajzX8Z1Wjm2WbWOhj0'
    SECRET_KEY = 'K71qqQKvxXHOlWrq4oVyg5Yvs28GpQD5'
    # 初始化对象
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    # 读取图片
    file_path = os.path.dirname(__file__)
    def get_file_content(file_path):
        with open(file_path, 'rb') as f:
            return f.read()

    image = get_file_content('./captcha1.png')
    # 定义参数变量
    options = {'language_type': 'ENG', }  # 识别语言类型，默认为'CHN_ENG'中英文混合
    #  调用通用文字识别
    result = client.basicAccurate(image, options)  # 高精度接口 basicAccurate
    for word in result['words_result']:
        captcha = (word['words'])

        print('识别结果：' + captcha)
    time.sleep(1)
    captchaInput = driver.find_element_by_xpath('//*[@id="ranstring"]')
    
    captchaInput.click()  
    captchaInput.clear()#.encode('utf-8')  
    captchaInput.send_keys(captcha)#.encode('utf-8')  

    loginButtum = driver.find_element_by_xpath('//*[@id="submit2"]') 
    loginButtum.click()


  
    
    #日历
    while 1:
        time.sleep(1)
        try:
            intoGradeButtum = driver.find_element_by_xpath('//*[@id="pageBodyRight"]/ul[1]/li[5]') 
            print('已定位到元素')
            break
        except:
            try:
                alertObject = driver.switch_to.alert  # 这里，alert方法不加括号，以为该方法被 @property 伪装成属性了，具体参考源码
                alertObject.accept()  # 点击确定按钮
                #验证码截图
                png = driver.find_element_by_xpath('//*[@id="randomPhoto"]/img')  # 查找验证码元素
                png.screenshot('capt.png')  # 对验证码进行截图并保存

                result = certify.aiocr()
                print(result)

                for word in result['words_result']:
                    captcha = (word['words'])

                    print('识别结果：' + captcha)

                captchaInput = driver.find_element_by_xpath('//*[@id="ranstring"]')
                captchaInput.click()  
                captchaInput.clear()#.encode('utf-8')

                while 1:
                    startTime = time.time()
                    time.sleep(1)
                    try:
                        captchaInput.send_keys(captcha)#.encode('utf-8')  
                        break
                    except:
                        if(time.time()-startTime)>10:
                            result = certify.aiocr()
                            for word in result['words_result']:
                                captcha = (word['words'])
                        else: 
                            print("等待验证码识别")

                loginButtum = driver.find_element_by_xpath('//*[@id="submit2"]') 
                loginButtum.click()
            except:
                print("还未定位到元素!")
    intoGradeButtum.click()

    driver.switch_to.frame('WindowFrame4')
    while 1:
        time.sleep(1)
        try:
            # nextButtum = driver.find_element_by_xpath('//*[@id="l_nav"]/ul/li[2]/a') 
            # nextButtum.click()
            followweekButtum = driver.find_element_by_xpath('html/body/div/div[2]/div[2]/div[1]/div/a') 
            print('已定位到元素')  
            end=time.time()  
            break
        except:
            print("还未定位到元素!")
    
    followweekButtum.click()
    
    options = driver.find_elements_by_tag_name('option')
    s1 = Select(driver.find_element_by_id('weekNo'))  # 实例化Select
    numOfOption = len(s1.options)
    excel_writer = pandas.ExcelWriter('schedule.xlsx')  # 定义writer，选择文件（文件可以不存在）
    totalTable = []
    for i in range(1,numOfOption):
        
        options = driver.find_elements_by_tag_name('option')
        s1 = Select(driver.find_element_by_id('weekNo'))
        s1.select_by_index(i)
        searchButtum = driver.find_element_by_xpath('//*[@id="r_content"]/div[2]/div[2]/table/tbody/tr[1]/td/form/span[1]/button') 
        searchButtum.click()
        
        locator = "//*[@id=\"r_content\"]/div[2]/div[2]/table"
        table = text_get_table_row_cell(driver,locator)
        totalTable.append(table)
        with open('table.json', mode='w', encoding='utf-8') as f:
            # 将字典列表存入json文件中
            info_str = json.dump(totalTable,sort_keys=False,ensure_ascii=False, separators=(',', ': '),fp=f)
    
    # calendar = ics.Calendar(calendar_name="22-23 SWJTU-Leeds")
    # with open('table.json', mode='r', encoding='utf-8') as f:
    #     totalTable = json.load(f)
    # for table in totalTable:
    #     calendar = ics.generateSchedule(calendar,table)
    #     calendar.save_as_ics_file()
    #     df = DataFrame(table)
    #     df.to_excel(excel_writer, sheet_name='df'+str(i), index=False)  # 写入指定表单
    # excel_writer.save()  # 储存文件
    # excel_writer.close()  # 关闭writer


    # calendar = ics.Calendar(calendar_name="test")
    # for table in totalTable:
    #     ics.generateSchedule(calendar,table)
    # calendar.save_as_ics_file()


if __name__=='__main__':


    isdebug = 1 #如果是1就在终端打印信息，如果是0就不打印
    
    if(isdebug==0):#默认不显示浏览器图形界面
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(chrome_options=chrome_options,executable_path="./chromedriver.exe")
    else:#如果是调试模式，则显示浏览器图形界面
        
        options = webdriver.ChromeOptions()
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option('excludeSwitches', ['enable-automation'])

        driver = webdriver.Chrome(chrome_options=options,executable_path="./chromedriver")
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
            })
            """
})
    time.sleep(1)
    search(driver,isdebug)

    while True:
        pass

