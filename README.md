# コマンドライン上でRSSを取得し続けるpy

ほとんどこちらからソースをいただきました。
[Search Make. 何か作りたいモノづくりサイト RSSを取得する ](http://make.bcde.jp/python/rss%E3%82%92%E5%8F%96%E5%BE%97%E3%81%99%E3%82%8B/)

feedparserのインストールはcondaを使って
`conda install feedparser`

ドキュメントはこちら
[feedparser 5.2.0 documentation](https://pythonhosted.org/feedparser/#)


```python:get_feed.py
from datetime import datetime
from time import mktime
import feedparser
from tqdm import tqdm
from time import sleep

# RSSのURL
RSS_URL = "http://www.fxstreet.jp/rss/news/forex-news/"

# RSSの取得
feed = feedparser.parse(RSS_URL)

# RSSのタイトル
print(feed.feed.title, '\n')


while True:
	try:
		for entry in tqdm(range(len(feed.entries))):
			# RSSの内容を一件づつ処理する
			title = feed.entries[entry].title
			link = feed.entries[entry].link

			# 更新日を文字列として取得
			published_string = feed.entries[entry].published

			# 更新日をdatetimeとして取得
			tmp = feed.entries[entry].published_parsed
			published_datetime = datetime.fromtimestamp(mktime(tmp))

			# 表示
			print(title)
			print(link)
			print(published_string)
			print(published_datetime)
			print('\n')
			sleep(1)
	except KeyboardInterrupt:
		break
```










## 追加した動作

* `while True:`で無限ループ
* `try-except`でctrl+cを押すまでループ
* `time.sleep(1)`で一エントリーにつき一秒おきに表示
* `tqdm.tqdm`で一周するまでにシーケンスバーを表示
	* tqdmはanacondaに入っていなかったのでこちらから取得
	* [conda-forge / Packages / tqdm 4.8.4](https://anaconda.org/conda-forge/* tqdm)


## TODO

* 複数RSSを巡回
* 一定時間経過 or 配信元で新しいnews配信されることで更新
* リンク先に本文があれば本文も表示(htmlパース)
* 文字列解析、データ化、集計、グラフ化


## BUGS

* ipython上では問題なく動くが、cmder上でエンコードエラー
`UnicodeEncodeError: 'cp932' codec can't encode character 
'\u20ac' in position 36: illegal multibyte sequence`
