# キーワード検索
# from apiclient.discovery import build
# from apiclient.errors import HttpError
# from oauth2client.tools import argparser
import argparse

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# 開発者用キー、使用するapiサービス名、バージョンを設定
DEVELOPER_KEY = "AIzaSyDsn7f6YJpuJSdh5yRlC_DLFSj3Ww7crXs" 
YOUTUBE_API_SERVICE_NAME = "youtube" 
YOUTUBE_API_VERSION = "v3"


# 要素を設定する
def arg_set(key_word='default', max_number=5):
    if key_word == 'default':
        print('キーワードを設定して下さい')
        return '検索キーワードを教えてください'
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('--q', help='Search term', default=key_word)
        print(type(max_number))
        parser.add_argument('--max-results', help='Max results', default=max_number)
        args = parser.parse_args()

        return args
    except Exception as e:
        print(f'エラー{e}')

def youtubeVideo_search(key_word, number:int) -> dict:
    
    # google apiの定義
    print('apiの初期化')
    youtube = build(YOUTUBE_API_SERVICE_NAME,
                  YOUTUBE_API_VERSION,
                  developerKey=DEVELOPER_KEY)

    # yotube apiで動画のキーワード検索
    print('apiを使う')
    search_response = youtube.search().list(
        q=key_word,
        part='id,snippet',
        maxResults=number).execute()

    videos = {}
    print_videos = []
    channels = []
    playlists = []

    print('取得した動画のトークナイズ')
    # 取得した動画情報をトークナイズする
    for search_result in search_response.get('items', []):
        # 動画のタイトルとUELを取得する
        if search_result['id']['kind'] == 'youtube#video':
            print_videos.append(f"Video Title：{search_result['snippet']['title']}\n \
                            Video URL:https://www.youtube.com/watch?v={search_result['id']['videoId']}\n")
            videos[f"Video Title:{search_result['snippet']['title']}"] = \
                f"Video URL:https://www.youtube.com/watch?v={search_result['id']['videoId']}"
        # 動画のタイトルとチャンネル名を取得する。
        # elif search_result['id']['kind'] == 'youtube#channel':
        #     channels.append('%s (%s)' % (search_result['snippet']['title'],
        #                                 search_result['id']['channelId']))
        # 動画のタイトルとプレイリスト名を取得する
        # elif search_result['id']['kind'] == 'youtube#playlist':
        #     playlists.append('%s (%s)' % (search_result['snippet']['title'],
        #                                     search_result['id']['playlistId']))

    # print('Videos:\n', '\n'.join(print_videos), '\n')
    # print('Channels:\n', '\n'.join(channels), '\n')
    # print('Playlists:\n', '\n'.join(playlists), '\n')

    return videos


if __name__ == '__main__':
    key_word = 'asmr'
    number = 5

    try:
        result = youtubeVideo_search(key_word, number)
        for k, v in result.items():
            print(k, v)
            print(f'*'*60)
    except HttpError as e:
        print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))