from flask import Flask, request, abort
import ast

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, PostbackEvent

from database.sqltest import Database

app = Flask(__name__)

# .env fileからアクセストークンとシークレットキーを取得する
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

access_token = os.environ.get('ACCESS_TOKEN')
secre_key = os.environ.get('SECRET_KEY')

line_bot_api = LineBotApi(access_token)
handler = WebhookHandler(secre_key)


# リクエストが正当なものか検証する
@app.route("/callback", methods=['POST'])
def callback():
    try:
        # シグネチャを取得する
        signature = request.headers['X-Line-Signature']

        # リクエスト内のbodyをテキストとして取得する
        body = request.get_data(as_text=True)
        print(f'bodyのなかみ:{body}')

        # シグネチャが正しいか検証する
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    
    return 'ok'

# ユーザの入力受け入れを可能、不能にするフラグを設定する。 ※ユーザごとに作った方が良いかも
# class GlobalFlag:
#     input_text = False


# イベントがメッセージイベント、メッセージがテキストだった時の処理
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    from youtube_api import search_videos
    try:
        
        databese = Database()
        reply_token = event.reply_token
        user_id = event.source.user_id

        # 入力受付が不可能の時
        # if GlobalFlag.input_text is False:
        #     line_bot_api.reply_message(
        #     reply_token,
        #     TextSendMessage(text='入力は不能です。リッチメニューを選択して入力して下さい。'))
        #     print(f' handle_message false input_text:{GlobalFlag.input_text}')
        #     return False
        jud = databese.get_inputText_bool(user_id=user_id)
        if jud is False:
            line_bot_api.reply_message(
            reply_token,
            TextSendMessage(text='入力は不能です。リッチメニューを選択して入力して下さい。'))
            return False

        # 入力が可能の時
        key_word = event.message.text
        print(f'user_idは{user_id}です')
        titles_videos = search_videos.youtubeVideo_search(key_word=key_word, number=2)

        print('ここまではOK')
        for title, video in titles_videos.items():
            return_text = f'title:{title}\n videos:{video}'
            line_bot_api.push_message(to=user_id, 
                                      messages=TextSendMessage(text=return_text))
            
        finish_text = '以上が動画とタイトルと動画になります。\nあなたの欲しい動画はありましたか？'
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=finish_text))
        # GlobalFlag.input_text = False
        # 入力受付を不能にする
        databese.update_inputText_bool(user_id=user_id, inputText_bool=False)

        return True

    except Exception as e:
        print(f'handle_message エラー発生{e}')


# イベントがpostbackだった時
@handler.add(PostbackEvent)
def handle_postback(event):
    print('Postback Eventはキャッチした')

    database = Database()
    reply_token = event.reply_token
    user_id = event.source.user_id
    postback_msg = event.postback.data

    try:
        if postback_msg == '入力を受け付ける':
            # 入力受付のためフラグをTrueにする。
            #GlobalFlag.input_text = True
            database.update_inputText_bool(user_id=user_id, inputText_bool=True)

            line_bot_api.reply_message(
                reply_token,
                messages=TextSendMessage(text='どうぞ欲しいvideoのタイトルを入力して下さい')
            )

    except Exception as e:
        print(e)


if __name__ == "__main__":
    pass
