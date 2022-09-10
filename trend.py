from math import ceil
import time

from bs4 import BeautifulSoup
import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.common.by import By


def startup():
    option = webdriver.ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-logging'])  # 鬱陶しいログを非表示にする
    option.add_argument('--headless')  # ヘッドレスモード(ウィンドウを非表示)
    driver = webdriver.Chrome(options=option)
    driver.get("https://scratch.mit.edu/explore/projects/all")
    time.sleep(0.5)
    return driver


def get_trends_by_num(start, end):
    """Scratchの傾向の作品のタイトルとIDを辞書型で返します。
    start引数とend引数に順位を指定してください。"""
    if start > end:
        raise ValueError("start引数はend引数より小さくしてください。")

    driver = startup()
    # 指定された順位が1Pより下ならそこまで表示させる
    if end - start >= 16:
        for j in range(ceil((end - start) / 16)):
            driver.find_element(By.XPATH, '//*[@id="projectBox"]/button/span').click()
            time.sleep(0.4)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    trend = list()

    for i in range(start, end):
        if i % 16 == 0:
            driver.find_element(By.XPATH, '//*[@id="projectBox"]/button/span').click()
            time.sleep(0.4)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
        # CSSセレクタで選択し、タイトルとIDを抽出
        found = soup.select_one(f"#projectBox > div > div > div:nth-of-type({i}) > div > div > a")
        project_data = {'title': found.contents[0], 'id': int(found.attrs['href'].replace("/", "").replace("projects", ""))}
        trend.append(project_data)
    return trend


def get_trends_by_page(start, end):
    """Scratchの傾向の作品のタイトルとIDを辞書型で返します。
    ページをstart引数とend引数に指定してください。"""
    if start > end:
        raise ValueError("start引数はend引数より小さくしてください。")

    driver = startup()
    # 指定されたページが2P以上なら表示させる
    if start >= 2:
        for i in range(start - 1):
            driver.find_element(By.XPATH, '//*[@id="projectBox"]/button/span').click()
            time.sleep(0.4)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    trend = list()

    for i in range((start - 1) * 16 + 1, end * 16 + 1):
        if i % 16 == 0:
            driver.find_element(By.XPATH, '//*[@id="projectBox"]/button/span').click()
            time.sleep(0.4)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
        # CSSセレクタで選択し、タイトルとIDを抽出
        # get_trends_by_num関数と同じ処理をしているので関数にしたかったがややこしくなるなのでしていない
        found = soup.select_one(f"#projectBox > div > div > div:nth-of-type({i}) > div > div > a")
        project_data = {'title': found.contents[0], 'id': int(found.attrs['href'].replace("/", "").replace("projects", ""))}
        trend.append(project_data)
    return trend


if __name__ == "__main__":
    # Test
    res = get_trends_by_page(start=1, end=3)
    print(*res, sep='\n')
    print(len(res))
