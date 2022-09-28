from math import ceil

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_binary


class ScratchTrend(object):
    """Scratchの傾向を取得します。
    Args:
        lang (str): 言語
        mode (int): 0が傾向、1は人気、2は最近です。
        hide (bool): ヘッドレスモードにするか
    """
    languages = (
        'ab', 'af', 'ar', 'am', 'an', 'ast', 'az', 'id', 'bn', 'be', 'bg', 'ca', 'cs', 'cy', 'da', 'de', 'et', 'el',
        'en', 'es', 'es-419', 'eo', 'eu', 'fa', 'fil', 'fr', 'fy', 'ga', 'gd', 'gl', 'ko', 'ha', 'hy', 'he', 'hr', 'xh',
        'zu', 'is', 'it', 'ka', 'kk', 'qu', 'sw', 'ht', 'ku', 'ckb', 'lv', 'lt', 'hu', 'mi', 'mn', 'nl', 'ja',
        'ja-Hira', 'nb', 'nn', 'oc', 'or', 'uz', 'th', 'km', 'pl', 'pt', 'pt-br', 'rap', 'ro', 'ru', 'nso', 'tn', 'sk',
        'sl', 'sr', 'fi', 'sv', 'vi', 'tr', 'uk', 'zh-cn', 'zh-tw')

    def __init__(self, lang: str, mode: int, hide: bool = True):
        if lang not in ScratchTrend.languages:
            raise ValueError("その言語には対応していません。")
        if mode > 3:
            raise ValueError("有効なモードを指定してください。")

        get_type = ("trending", "popular", "recent")

        self.__cookie = {"name": "scratchlanguage", "value": lang}
        self._mode = get_type[mode]
        self.__hide = hide

    def _setup(self):
        """Chromeの起動などをします。
        Run Chrome.
        """

        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        if self.__hide:
            options.add_argument('--headless')

        driver = webdriver.Chrome(options=options)
        driver.get("https://scratch.mit.edu/explore/projects/all")
        driver.add_cookie(self.__cookie)
        driver.get(
            f"https://scratch.mit.edu/explore/projects/all/{self._mode}")
        WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located)

        return driver

    def get_by_num(self, start: int, end: int) -> list:
        """順位を指定して取得します。

        Args:
            start (int): 最初の順位
            end (int): 最後の順位

        Raises:
            ValueError: start>end の時

        Returns:
            list[dict]: リスト内辞書
        """

        if start > end:
            raise ValueError("start引数はend引数より小さくしてください。")

        driver = self._setup()
        # 指定された順位が1Pより下のときの処理
        if end - start >= 17:
            for j in range(ceil((end - start) / 16)):
                driver.find_element(
                    By.XPATH, '//*[@id="projectBox"]/button').click()

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        trend = list()

        for i in range(start, end):
            selector = f"#projectBox > div > div > div:nth-of-type({i}) > div > div > a"
            if i % 16 == 0:
                driver.find_element(
                    By.XPATH, '//*[@id="projectBox"]/button').click()
                # 少し無理やりです
                driver.implicitly_wait(10)
                driver.find_element(By.CSS_SELECTOR, selector)
                soup = BeautifulSoup(driver.page_source, 'html.parser')

            # CSSセレクタで選択し、タイトルとIDを抽出
            found = soup.select_one(selector)
            project_data = {'title': found.text, 'id': int(
                found.attrs['href'].replace("/", "").replace("projects", ""))}
            trend.append(project_data)

        return trend

    def get_by_page(self, start: int, end: int) -> list:
        """ページを指定して取得します。

        Args:
            start (int): 最初のページ
            end (int): 最後のページ

        Raises:
            ValueError: start>end の時

        Returns:
            list[dict]: リスト内辞書
        """

        if start > end:
            raise ValueError("start引数はend引数より小さくしてください。")

        driver = self._setup()
        # 指定されたページが2P以上なら表示させる
        if start >= 2:
            for i in range(start - 1):
                driver.find_element(
                    By.XPATH, '//*[@id="projectBox"]/button').click()
                driver.implicitly_wait(1.5)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        trend = list()

        for i in range((start - 1) * 16 + 1, end * 16 + 1):
            selector = f"#projectBox > div > div > div:nth-of-type({i}) > div > div > a"

            if i % 16 == 0:
                driver.find_element(
                    By.XPATH, '//*[@id="projectBox"]/button').click()
                driver.implicitly_wait(10)
                driver.find_element(
                    By.CSS_SELECTOR, selector.replace(str(i), str(i+1)))

                soup = BeautifulSoup(driver.page_source, 'html.parser')

            # CSSセレクタで選択し、タイトルとIDを抽出
            found = soup.select_one(selector)
            project_data = {'title': found.text, 'id': int(
                found.attrs['href'].replace("/", "").replace("projects", ""))}
            trend.append(project_data)

        return trend


if __name__ == "__main__":
    import time

    timer = time.perf_counter()
    res = ScratchTrend("ja", 0, True).get_by_num(1, 100)
    timer_end = time.perf_counter()

    print(*res, sep='\n')
    print(len(res))
    print(f"所要時間:{timer_end - timer}")
