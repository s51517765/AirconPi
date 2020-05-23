# -*- coding: utf-8 -*-
from slackbot.bot import Bot
import datetime as dt
import bme280
# https://qiita.com/sukesuke/items/1ac92251def87357fdf6


'''
slackbot         # プログラムをまとめるディレクトリ。名前はなんでも良い
├─ slackBot.py        # このプログラムを実行することで、ボットを起動する
├─ slackbot_settings.py   # botに関する設定を書くファイル
└─ plugins                # mensionに対する応答の定義
└─ airconSet.py           # GPIOの定義と動作
└─ bme280.py              # 環境センサの動作
'''


def main():
    # Main スクリプト
    print("SlackBot start!")
    tdatetime = dt.datetime.now()
    print(tdatetime)
    bot = Bot()
    bot.run()


if __name__ == "__main__":
    main()
