import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import line_notify

# 最終出力要の配列を初期化
data_list = []

# WebDriverの起動（Chromeの例）
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('C:\driver\chromedriver_win32\chromedriver',options=options)

# 取得対象のURLを指定
url = 'https://reserve.karadabesta.jp/reserve/schedule/2/2/'

# ウェブページへのアクセス
driver.get(url)
#指定したdriverに対して最大で10秒間待つように設定する
wait = WebDriverWait(driver, 10)
time.sleep(3)

#指定したボタンが表示されクリック出来る状態になるまで待機する
wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '//*[@id="__layout"]/div/div[1]/section/section/div[2]/div[3]/div/div[2]/div')))
# 「【会員様向け】 パーソナルトレーニング予約メニュー」をクリックする
click_0 = driver.find_element(by=By.XPATH, value='//*[@id="__layout"]/div/div[1]/section/section/div[2]/div[3]/div/div[2]/div')
click_0.click()
time.sleep(3)

for traner_num in range(1,7):
    #指定したボタンが表示されクリック出来る状態になるまで待機する
    wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '//*[@id="__layout"]/div/div[1]/section/section/div[2]/div[3]/div[2]/div[2]/div[' + str(traner_num) + ']')))
    # 担当者を選択する
    click_open = driver.find_element(by=By.XPATH, value='//*[@id="__layout"]/div/div[1]/section/section/div[2]/div[3]/div[2]/div[2]/div[' + str(traner_num) + ']')
    # 範囲外がクリックできないので、JavaScriptを使用してクリックする
    driver.execute_script("arguments[0].click();", click_open)
    # click_open.click()
    time.sleep(2)

    # 担当者名を取得する
    traner_name = driver.find_element(by=By.XPATH, value='//*[@id="__layout"]/div/div[1]/section/section/div[2]/div[3]/div[2]/div/div[2]').text

    # 日付、曜日を取得する
    day_list = []
    for day in range(2,9):
        get_day = driver.find_element(by=By.XPATH, value='//*[@id="__layout"]/div/div[1]/section/section/div[2]/div[3]/div[3]/div/div[1]/div[2]/div/div[' + str(day) + ']')
        day_text = get_day.text
        # 改行コードを削除する
        day_text = "".join(day_text.splitlines())
        day_list.append(day_text)

    # 時間のリストを取得する
    time_list = []
    for time_value in range(1,33):
        get_time_value = driver.find_element(by=By.XPATH, value='//*[@id="__layout"]/div/div[1]/section/section/div[2]/div[3]/div[3]/div/div[2]/div/div[' + str(time_value) + ']/div[1]')
        time_value_text = get_time_value.text
        time_list.append(time_value_text)

    # 日にちごとの空き状況リストを作成する
    availability_list = []
    for week in range(2,9):
        # 一時テーブルなので、随時初期化
        availability_list_unit = []
        for availability in range(1,33):
            # 1日分
            get_availability = driver.find_element(by=By.XPATH, value='//*[@id="__layout"]/div/div[1]/section/section/div[2]/div[3]/div[3]/div/div[2]/div/div[' + str(availability) + ']/div[' + str(week) + ']')
            availability_text = get_availability.text
            # 予約可能な場合、値が入っていないので、「担当者」を代入してあげる
            if availability_text == '':
                availability_text = traner_name
            availability_list_unit.append(availability_text)
        availability_list.append(availability_list_unit)

    # 日付、時間、空き状況のリストを作る
    data_list_all = pd.DataFrame(data=availability_list,index=day_list,columns=time_list)

    list_index = []
    list_columns = []
    list_index = list(data_list_all.index)
    list_columns = list(data_list_all.columns)

    for index_name in list_index:
        for columns_name in list_columns:
            list_value = data_list_all.at[index_name, columns_name]
            if list_value != '-':
                data_list.append(index_name + " " + columns_name + ":" + list_value)

    # 担当者を閉じる
    click_close = driver.find_element(by=By.XPATH, value='//*[@id="__layout"]/div/div[1]/section/section/div[2]/div[3]/div[2]/div')
    click_close.click()
    time.sleep(2)

data_list_sort = sorted(data_list)

# LINE通知をする
line_notify.send_line_notify(data_list_sort)
