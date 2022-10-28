<div align="center"><img src="https://user-images.githubusercontent.com/105550500/197376654-a36e55d0-35ac-42c8-aed5-23e9a48c04fd.jpg" /></div>

# ScratchTrend: Scratchから人気作品を取得。
[![PyPI](https://img.shields.io/badge/PyPI-dummy?style=for-the-badge&logo=pypi&labelColor=gray&color=red)](https://pypi.org/project/scratchtrend/)
[![GitHub](https://img.shields.io/badge/GitHub-dummy?style=for-the-badge&logo=github&labelColor=gray&color=blue)](https://pypi.org/project/scratchtrend/)

[![Licence](https://img.shields.io/github/license/henji243/ScratchTrend)](https://github.com/henji243/ScratchTrend)
[![Downloads](https://img.shields.io/pypi/dd/scratchtrend?color=%2383ccd2&label=PyPI%20Downloads&logo=PyPI&logoColor=%2383ccd2)](https://pypi.org/project/scratchtrend)

ScratchTrendは、https://scratch.mit.edu/explore から、人気の作品を取得します。
<br />
<span style="color: red;">**(このライブラリはScratch財団とは無関係です。)**</span>
<br /><br />
# 使い方
## インストール
ターミナル
```sh
$ pip install scratchtrend
```
インポート
```python
import scratchtrend as sct
from scratchtrend.select import Lang, Sort
```

## 準備
```python
# example
data = sct.connect(Lang.JAPANESE, Sort.POPULAR)
```
指定できる言語の一覧はLanguages.mdに書いてあります。
```connect()```メソッドで、言語、並び替えを指定してください。<br />
並び替えは以下の通りです:
| 指定内容 | 並び替え |
| ------- | ------- |
| Sort.TRENDING | 傾向 |
| Sort.POPULAR | 人気 |
| Sort.RECENT | 最近 |

## メソッド
(まだ開発途中のため、ショボいです)
```python
data.get_by_page()  # ページを指定して取得
data.get_by_num()  # 順位(←少し語弊があります)を指定して取得
```
```get_by_page()```はstart引数からend引数のページの作品を取得します。必ず start&lt;endとなるようにしてください。
```get_by_num()```はstart引数からend引数の順位の作品を取得します。こちらもstart&lt;endとなるようにしてください。<span style="font-size: 50%;">"順位"という言い方には少し語弊があります。良い言い方があったらIssuesまで。</span>
