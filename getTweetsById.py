import os
import re
from twitter_scraper import get_tweets


def formatText(tweets):
# 取得したツイートを出力可能な状態に整形してあげる関数
    con = 0
    return_text = ""
    for tweet in tweets:
        # ハッシュタグやリンクを削除
        output_text = re.sub(r'pic.*','',tweet['text'])
        output_text = re.sub(r'#.*','',output_text)
        output_text = re.sub(r'http.*','',output_text)
        # 文末に読点がなければ挿入して、あればそのまま改行を削除
        output_text = re.sub(r'。\n','。',output_text)
        output_text = re.sub(r'\n','。',output_text)
        # print('==== OrigineText ====\n{}'.format(tweet['text']))
        # print(re.sub(r'pic.*','',tweet['text']))
        # print('==== outputText ====\n{}'.format(output_text))
        con = con + 1
        return_text += output_text
    return return_text


def main(tweets):
# ファイルに書き出す関数
    output = formatText(tweets)
    with open('tweet.txt', 'a') as f:
        f.write(output)


if __name__ == '__main__':
# エントリーポイント
    TwitterID = input('input Twitter ID without @ mark >> ')

    # TwitterID = re.sub
    main(get_tweets(TwitterID, pages=5, unget_retweet=False))
