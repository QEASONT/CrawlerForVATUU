from aip import AipOcr
from PIL import Image
import os
def aiocr():
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
    return result