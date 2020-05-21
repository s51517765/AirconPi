# -*- coding: utf-8 -*-
from slackbot.bot import respond_to, listen_to
import re
import time
from datetime import datetime as dt
import os
if str(os.path).find("Projects") == -1 and str(os.path).find("Users") == -1:  # path名からPCを判定
    import airconSet
    import bme280
else:
    print("wiringpi is passed! ")


@listen_to(u'.*(now|今|すぐ).*')
@respond_to(u'.*(now|今|すぐ).*')
def timerReset(message, something):
    try:
        text = message.body['text']
        if "on" in text or "off" in text or "power" in text:
            airconSet.aircon_power()
            message.reply("電源を操作しました。")
        elif "up" in text or "上" in text:
            airconSet.aircon_temp_set_up(1)
            message.reply("温度設定を +1 しました。")
        elif "down" in text or "下" in text:
            airconSet.aircon_temp_set_down(1)
            message.reply("温度設定を -1 しました。")
    except NameError as e:
        print(e)
        message.reply("NameError. airconSet.py")
    except Exception as e:
        message.reply("指示を解釈できませんでした。")


@listen_to(u'\d*?(上|up|下|down)\d*?')  # up +スペース+数字 スペースは省略可能
@respond_to(u'\d*?(上|up|下|down)\d*?')
def OrderUpDown(message, something):
    try:
        # someting = 反応したword
        text = message.body['text']
        text = text.split()
        timeSet = None
        tempertureSet = None
        for i in text:
            if re.match(r'[0-9]{1}', i) != None:  # 正規表現にマッチするものがあるかどうか
                if len(i) == 4:
                    timeSet = i
                elif len(i) == 1:
                    tempertureSet = i

        hh = timeSet[:2]
        mm = timeSet[2:]
        hh = int(hh)
        mm = int(mm)
        if hh > 24:
            raise ValueError("error!")
        if mm > 59:
            mm = 59

        # 命令を出したユーザ名を取得
        userID = message.channel._client.users[message.body['user']][u'name']

        tdatetime = dt.now()
        if something == "up" or something == "上":
            airconSet.set(hh, mm, tempertureSet, "up")
            message.reply("時刻" + timeSet + "に" +
                          tempertureSet + "℃上げるようにセットしました。")
        elif something == "down" or something == "下":
            airconSet.set(hh, mm, tempertureSet, "down")
            message.reply("時刻" + timeSet + "に" +
                          tempertureSet + "℃下げるようにセットしました。")
        print(tdatetime, "accept oder from ", userID, )
    except NameError as e:
        print(e)
        message.reply("NameError. airconSet.py")
    except Exception as e:
        message.reply("セットできませんでした。タイマーセットの入力書式は hhmm temp up/down です")


@listen_to(u'(reset|リセット|削除|delete)+')
@respond_to(u'(reset|リセット|削除|delete)+')
def timerReset(message, something):
    try:
        text = message.body['text']
        airconSet.timer_remove()
        message.reply("タイマー設定を削除しました。")
    except NameError as e:
        print(e)
        message.reply("NameError. airconSet.py")
    except Exception as e:
        print(e)
        message.reply("指示を解釈できませんでした。")


@listen_to(u'(start|スタート)+')
@respond_to(u'(start|スタート)+')
def timerStart(message, something):
    try:
        text = message.body['text']
        message.reply("タイマースタートしました。")
        airconSet.timer()
    except Exception as e:
        print(e)
        message.reply("指示を解釈できませんでした。")


@listen_to(u'(set|設定)+')
@respond_to(u'(set|設定)+')
def call_setting(message, something):
    try:
        text = airconSet.show_setting()
        message.reply(text)
    except Exception as e:
        print(e)
        message.reply("指示を解釈できませんでした。")


@listen_to(u'(help|ヘルプ|助け)+')
@respond_to(u'(help|ヘルプ|助け)+')
def help(message, something):
    try:
        message.reply(
            "タイマーセット→ hhmm temp up/down。　タイマー設定の削除→ リセット、タイマースタート→ スタート。設定時刻確認→ 設定。動き出したタイマーを止めるにはストップボタンを押してください。 温湿度確認→温度。")
    except Exception as e:
        print(e)
        message.reply("指示を解釈できませんでした。")


@listen_to(u'(温|temp|湿|環)+')
@respond_to(u'(温|temp|湿|環)+')
def temp(message, something):
    try:
        env_result = bme280.main()
        message.reply(env_result)
    except NameError as e:
        print(e)
        message.reply("NameError. airconSet.py")
    except Exception as e:
        print(e)
        message.reply("指示を解釈できませんでした。")


# @respond_to('string')     bot宛のメッセージ
#                           stringは正規表現が可能 「r'string'」
# @listen_to('string')      チャンネル内のbot宛以外の投稿
#                           @botname: では反応しないことに注意
#                           他の人へのメンションでは反応する
#                           正規表現可能
# @default_reply()          DEFAULT_REPLY と同じ働き
#                           正規表現を指定すると、他のデコーダにヒットせず、
#                           正規表現にマッチするときに反応
#                           ・・・なのだが、正規表現を指定するとエラーになる？

# message.reply('string')      @発言者名: string でメッセージを送信
# message.send('string')       string を送信
# message.react('icon_emoji')  発言者のメッセージにリアクション(スタンプ)する
#                              文字列中に':'はいらない
