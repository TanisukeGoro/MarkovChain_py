import re
from requests_html import HTMLSession, HTML
from datetime import datetime

session = HTMLSession()


def get_tweets(user, pages=25, unget_retweet=True):
    """ Argment
        user  : Twitter ID without @ mark
        pages : number of Scraping pages
        unget_retweet : include retweets or not
    """
    """Gets tweets for a given user, via the Twitter frontend API."""


    url = f'https://twitter.com/i/profiles/show/{user}/timeline/tweets?include_available_features=1&include_entities=1&include_new_items_bar=true'
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': f'https://twitter.com/{user}',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8',
        'X-Twitter-Active-User': 'yes',
        'X-Requested-With': 'XMLHttpRequest'
    }
    def gen_tweets(pages):
        r = session.get(url, headers=headers)

        while pages > 0:
            try:
                html = HTML(html=r.json()['items_html'],
                            url='bunk', default_encoding='utf-8')
            except KeyError:
                raise ValueError(
                    f'Oops! Either "{user}" does not exist or is private.')

            comma = ","
            dot = "."
            tweets = []
            for tweet in html.find('.stream-item'):
                # よくわからんがエラーが起きるから
                try:
                    # ツイート元のtwitterIDを取得
                    twitterId = tweet.find('.js-stream-tweet')[0].attrs['data-screen-name']
                except IndexError:
                    continue

                if unget_retweet or user == twitterId:
                    text = tweet.find('.tweet-text')[0].full_text
                    tweetId = tweet.find(
                        '.js-permalink')[0].attrs['data-conversation-id']

                    time = datetime.fromtimestamp(
                        int(tweet.find('._timestamp')[0].attrs['data-time-ms'])/1000.0)
                    # print('time: ' + str(time)) #instart


                    interactions = [x.text for x in tweet.find(
                        '.ProfileTweet-actionCount')]

                    # 空の要素には'0'を挿入する。
                    interactions = ['0' if i == '' else i for i in interactions]

                    replies = int(interactions[3].split(" ")[0]
                        .replace(comma, "").replace(dot,""))



                    retweets = int(interactions[4].split(" ")[0]
                        .replace(comma, "").replace(dot,""))


                    likes = int(interactions[6].split(" ")[0]
                        .replace(comma, "").replace(dot,""))



                    hashtags = [hashtag_node.full_text for hashtag_node in tweet.find('.twitter-hashtag')]
                    urls = [url_node.attrs['data-expanded-url'] for url_node in tweet.find('a.twitter-timeline-link:not(.u-hidden)')]
                    photos = [photo_node.attrs['data-image-url'] for photo_node in tweet.find('.AdaptiveMedia-photoContainer')]

                    videos = []
                    video_nodes = tweet.find(".PlayableMedia-player")
                    for node in video_nodes:
                        styles = node.attrs['style'].split()
                        for style in styles:
                            if style.startswith('background'):
                                tmp = style.split('/')[-1]
                                video_id = tmp[:tmp.index('.jpg')]
                                videos.append({'id': video_id})
                    tweets.append({'tweetId': tweetId, 'time': time, 'text': text,
                                   'replies': replies, 'retweets': retweets, 'likes': likes,
                                   'entries': {
                                        'hashtags': hashtags, 'urls': urls,
                                        'photos': photos, 'videos': videos
                                    }
                                   })

            last_tweet = html.find('.stream-item')[-1].attrs['data-item-id']

            for tweet in tweets:
                if tweet:
                    tweet['text'] = re.sub('http', ' http', tweet['text'], 1)
                    yield tweet

            r = session.get(
                url, params = {'max_position': last_tweet}, headers = headers)
            pages += -1

    yield from gen_tweets(pages)
