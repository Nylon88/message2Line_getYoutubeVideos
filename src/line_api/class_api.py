from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# .env fileからアクセストークンとシークレットキーを取得する
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


class LineApiClass:
    access_token = os.environ.get('ACCESS_TOKEN')
    secre_key = os.environ.get('SECRET_KEY')

    line_bot_api = LineBotApi(access_token)
    handler = WebhookHandler(secre_key)

class Message(LineApiClass):
    def __init__(self) -> None:
        super().__init__()
    
    


class RichMenu(LineApiClass):
    def __init__(self) -> None:
        super().__init__()

    # 画像をアップロードする
    def upload_picture(self, pic_path:str) -> str:
        with open(pic_path, 'rb') as f:
            LineApiClass.line_bot_api.set_rich_menu_image('richmenu-61863fe821d7ae29468f3b185c275f72', 'image/jpeg', f)
        
        return 'ok'

    # リッチメニューIDを取得する
    def get_rich_menu_list(self) -> list:
        response = LineApiClass.line_bot_api.get_rich_menu_list()
        return response


if __name__ == '__main__':
    richmenu = RichMenu()
    richmenu.get_rich_menu_list()




