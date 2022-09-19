from math import ceil
import time

from bs4 import BeautifulSoup
import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class trend_data(object):
    def setup(self):
        option = webdriver.ChromeOptions()
        option.add_experimental_option('excludeSwitches', ['enable-logging'])  # ログを非表示にする
        option.add_argument('--headless')  # ヘッドレスモード(ウィンドウを非表示)
        driver = webdriver.Chrome(options=option)
        driver.get("https://scratch.mit.edu/explore/projects/all")

        wait = WebDriverWait(driver, 20)  # 待機処理
        wait.until(EC.presence_of_all_elements_located)
        return driver, wait

    def get_trends_by_num(self, start, end):
        """Scratchの傾向の作品のタイトルとIDを辞書型で返します。
        start引数とend引数に順位を指定してください。

        start引数からend引数の順位の作品を取得します。"""

        if start > end:
            raise ValueError("start引数はend引数より小さくしてください。")

        driver, wait = self.setup()
        # 指定された順位が1Pより下ならそこまで表示させる
        if end - start >= 16:
            for j in range(ceil((end - start) / 16)):
                driver.find_element(By.XPATH, '//*[@id="projectBox"]/button/span').click()
                driver.implicitly_wait(1.5)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        trend = list()

        for i in range(start, end):
            selector = f"#projectBox > div > div > div:nth-of-type({i}) > div > div > a"
            if i % 16 == 0:
                driver.find_element(By.XPATH, '//*[@id="projectBox"]/button/span').click()
                # 少し無理やりです
                driver.implicitly_wait(10)
                driver.find_element(By.CSS_SELECTOR, selector.replace(str(i), str(i+1)))
                soup = BeautifulSoup(driver.page_source, 'html.parser')

            # CSSセレクタで選択し、タイトルとIDを抽出
            found = soup.select_one(f"#projectBox > div > div > div:nth-of-type({i}) > div > div > a")
            project_data = {'title': found.contents[0], 'id': int(
                found.attrs['href'].replace("/", "").replace("projects", ""))}
            trend.append(project_data)
        return trend

    def get_trends_by_page(self, start, end):
        """Scratchの傾向の作品のタイトルとIDを辞書型で返します。
        ページをstart引数とend引数に指定してください。"""
        if start > end:
            raise ValueError("start引数はend引数より小さくしてください。")

        driver, wait = self.setup()
        # 指定されたページが2P以上なら表示させる
        if start >= 2:
            for i in range(start - 1):
                driver.find_element(By.XPATH, '//*[@id="projectBox"]/button/span').click()
                driver.implicitly_wait(1.5)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        trend = list()

        for i in range((start - 1) * 16 + 1, end * 16 + 1):
            selector = f"#projectBox > div > div > div:nth-of-type({i}) > div > div > a"
            if i % 16 == 0:
                driver.implicitly_wait(10)
                driver.find_element(By.XPATH, '//*[@id="projectBox"]/button/span').click()
                driver.implicitly_wait(10)
                driver.find_element(By.CSS_SELECTOR, selector.replace(str(i), str(i+1)))
                soup = BeautifulSoup(driver.page_source, 'html.parser')

            # CSSセレクタで選択し、タイトルとIDを抽出
            found = soup.select_one(selector)
            project_data = {'title': found.contents[0], 'id': int(
                found.attrs['href'].replace("/", "").replace("projects", ""))}
            trend.append(project_data)
        return trend


if __name__ == "__main__":
    timer = time.perf_counter()
    res = trend_data().get_trends_by_num(1, 100)
    timer_end = time.perf_counter()
    print(*res, sep='\n')
    print(len(res))
    print(f"所要時間:{timer_end-timer}")
