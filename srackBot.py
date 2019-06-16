# -*- coding: utf-8 -*-
from slackbot.bot import Bot
#https://qiita.com/sukesuke/items/1ac92251def87357fdf6

# 個人用

'''
slackbot         # プログラムをまとめるディレクトリ。名前はなんでも良い
├─ slackBot.py        # このプログラムを実行することで、ボットを起動する
├─ slackbot_settings.py   # botに関する設定を書くファイル
└─ plugins                # mensionに対する応答の定義
└─ airconSet.py           # GPIOの定義と動作
'''

# Main スクリプト

bot = Bot()
bot.run()

