# 概要
APIを使わずに作品のタイトルとIDを取得します。
無限(たぶん)に取得できます。Seleniumで移動→BeautifulSoupでスクレイピングして取得します。
# 必要なライブラリ(モジュール?)
- Selenium(作成時は4.4.0)
- Beautifulsoup4(作成時は4.11.1)
- chromedriver_binary(作成時は104.0.5112.79.0)
- Google Chrome(~誰でもいれてるはず~)

chromedriver_binaryはSeleniumが使用できるなら47行目を```webdriver.Chrome(executable_path='ChromeDriverのPath', options=option)```にしてもらえればOKです
# 使い方
```get_by_num()```メソッドでは、start引数からend引数の順位を取得します。
```get_by_page()```メソッドでは、start引数からend引数のページの作品を全て取得します。
<br />
<br />
<br /><!-- HTMLのタグ使えるんだ -->
<br />
<br />
# 余談
前までBeautifulSoupのことをビューティフルソープって読んでたけど最近ビューティフル **スープ** とわかった。
どっちにしろなんでそういう名前にしてのだろうか()
