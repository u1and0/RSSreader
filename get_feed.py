# coding: utf-8
'''
# コマンドライン上でRSSを取得し続けるpy

feature/html


## 追加した動作

feature/html
* 文法をPEP8に準拠
* エラー発生時にメッセージ見れるようsleep関数有効化

develop
* `while True:`で無限ループ
* `try-except`でctrl+cを押すまでループ
* `time.sleep(1)`で一エントリーにつき一秒おきに表示
* `tqdm.tqdm`で一周するまでにシーケンスバーを表示
    * tqdmはanacondaに入っていなかったのでこちらから取得
    * [conda-forge / Packages / tqdm 4.8.4](https://anaconda.org/conda-forge/* tqdm)


## TODO

* リンク先に本文があれば本文も表示
    - 複数RSSを巡回
    * 一定時間経過 or 配信もとで新しいnews配信されることで更新
    * 文字列解析、データ化、集計、グラフ化


## BUGS

'''
from datetime import datetime
from time import mktime
import feedparser
from tqdm import tqdm
from time import sleep

# RSSのURL
RSS_URL = (
    'http://freesoft-100.com/rss.xml',
    # 'http://www.vector.co.jp/rss/softnews.xml',
    # 'http://www.forest.impress.co.jp/rss.xml',
    # 'http://www.gigafree.net/index.xml',
    # 'http://freesoftbangai.blog50.fc2.com/?xml',
    # 'http://www.softnavi.com/rss.xml',
    # 'http://mozilla-remix.seesaa.net/index.rdf',
    # 'http://matt.livedoor.biz/index.rdf',
    # 'http://fxgaitame1.blog89.fc2.com/?xml',
    # 'http://news.finance.yahoo.co.jp/rss/cp/fisf.xml',
    # 'http://blog.livedoor.jp/fwht9851/index.rdf',
    # 'http://www.fxstreet.com/xml/rss20.xml',
    # 'http://feeds.reuters.com/reuters/JPBusinessNews',
    # 'http://mainasusikouonna.blog34.fc2.com/?xml',
    # 'http://kumafx.seesaa.net/index.rdf',
    # 'http://www.fxstreet.jp/rss/news/forex-news/',
    # 'http://usdjpy-fxyosou.blog.jp/index.rdf',
    # 'http://markethack.net/index.rdf',
    # 'http://fxforex.seesaa.net/index.rdf',
    # 'http://nursefx.blog.fc2.com/?xml',
    # 'http://zai.diamond.jp/list/feed/rssfxnews',
    # 'http://www.kanetsufx.co.jp/rss/shikyo.xml',
    # 'http://jp.wsj.com/xml/rss/3_9740.xml',
    # 'http://news.nicovideo.jp/topiclist?rss=2.0',
    # 'http://rss.dailynews.yahoo.co.jp/fc/rss.xml',
    # 'http://www.jiji.com/rss/ranking.rdf',
    # 'http://www.zou3.net/php/rss/nikkei2rss.php?head=main',
    # 'http://jp.wsj.com/xml/rss/3_9743.xml',
    # 'http://jp.wsj.com/xml/rss/3_9742.xml',
    # 'http://www3.nhk.or.jp/rss/news/cat0.xml',
    # 'http://slashdot.jp/slashdotjp.rss',
    # 'http://feeds.reuters.com/reuters/JPTopNews',
    # 'http://sankei.jp.msn.com/rss/news/points.xml',
    # 'https://k.xpg.jp/feed.xml',
    # 'http://www.lifehacker.jp/index.xml',
    # 'http://hotentry.hatenablog.jp/feed/category/週刊ネタ',
    # 'http://wired.jp/feed/',
    # 'http://b.hatena.ne.jp/hotentry.rss',
    # 'http://readingmonkey.blog45.fc2.com/?xml',
    # 'http://webdesign-manga.com/feed/',
    # 'http://pinkyforgirls.com/feed/',
    # 'http://blog-kota.sblo.jp/index.rdf',
    # 'http://nomad-ken.com/feed',
    # 'http://gigazine.net/index.php?/news/rss_2.0/',
    # 'http://kazu22002.hatenablog.com/feed',
    # 'http://d.hatena.ne.jp/Chikirin/rss',
    # 'https://github.com/blog.atom',
    # 'http://wbond.net/sublime_packages/community/rss',
    # 'https://www.oreilly.com/topics/open-source/feed.atom',
    # 'http://www.oreilly.co.jp/ebook/new_release.atom',
    # 'http://planet.python.org/rss10.xml',
    # 'http://api.plaza.rakuten.ne.jp/kabu1000/rss/',
    # 'http://zhirozzz2999.seesaa.net/index.rdf',
    # 'http://www.tradernews.jp/kabu/feed.xml',
    # 'http://blog.livedoor.jp/ikagawa4/index.rdf',
    # 'http://rssblog.ameba.jp/fumufu2000/rss20.xml',
    # 'http://yamikabu.blog136.fc2.com/?xml',
    # 'http://money-goround.jp/feed/',
    # 'http://column.ifis.co.jp/feed',
    # 'http://blog.livedoor.jp/kabu2oku/index.rdf',
    # 'http://kabooo.net/index.rdf',
    # 'http://api.plaza.rakuten.ne.jp/www9945/rss/'
)

while True:
    for url in RSS_URL:
        # RSSの取得
        feed = feedparser.parse(url)

        error_count = 0
        try:
            # RSSのタイトル
            print(feed.feed.title, '\n')

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
                # sleep(1)
        except KeyboardInterrupt:
            break
        except AttributeError as e:
            print('! Exception :', e.args)
            sleep(2)
            error_count += 1
        except:
            error_count += 1
            # pass
        finally:
            print('Error occured', error_count)
    else:
        pass
