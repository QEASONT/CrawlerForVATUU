def text_get_table_row_cell(driver, locator):
    """通过xpath定位的方式，根据参数text中的文本返回文本所在的行列"""

    # 获取行数，由于部分表格表头是用th而不是用td，可能会出现计算错误。因此这里先除去表头
    table_tr = driver.find_elements_by_xpath(locator + "/tbody/tr[3]/td/table/tbody/tr")[0:]
    row = len(table_tr)

    # 获取列数
    table_td = driver.find_elements_by_xpath(locator + "/tbody/tr[3]/td/table/tbody/tr/td")
    col = int(len(table_td)/row)
    # 遍历table中的所有文本，并匹配的值返回所在的行列
    # xpath中下标取值从1开始，除去表头，需要从2开始
    table = []
# //*[@id="r_content"]/div[2]/div[2]/table/tbody/tr[3]/td/table/tbody/tr[1]/td[1]
# //*[@id="r_content"]/div[2]/div[2]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[1]
# //*[@id="r_content"]/div[2]/div[2]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]
# //*[@id="r_content"]/div[2]/div[2]/table/tbody/tr[3]/td/table/tbody/tr[3]/td[1]
    for i in range(1, row + 1):
        table_row = []
        for j in range(1, col + 1):
            tl = locator + "/tbody/tr[3]/td/table/tbody/tr[" + str(i) + "]/td[" + str(j) + "]"
            table_row.append([driver.find_element_by_xpath(tl).text])
        table.append(table_row)
    return table
