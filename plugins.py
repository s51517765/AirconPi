# -*- coding: utf-8 -*-
from slackbot.bot import respond_to, listen_to
import re
from datetime import datetime as dt
import airconSet


@listen_to(u'(now|今|すぐ)+')
@respond_to(u'(now|今|すぐ)+')
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
    except Exception as e:
        print(e)
        message.reply("指示を解釈できませんでした。")


@listen_to(u'(上|up|下|down)\s?\d')  # up +スペース+数字 スペースは省略可能
@respond_to(u'(上|up|下|down)\s?\d')
def OrderUpDown(message, something):
    try:
        # someting = 反応したword
        text = message.body['text']
        text = text.replace(something, "")  # 起動ワードを削除
        timeSet = re.search('[0-9]{4}', text)
        timeSet = timeSet.group(0)
        hh = timeSet[:2]
        mm = timeSet[2:]
        hh = int(hh)
        mm = int(mm)
        if hh > 24:
            raise ValueError("error!")
        if mm > 59:
            mm = 59
        text = re.sub('[0-9]{4}', "", text)
        tempertureSet = re.search('[0-9]{1}', text)
        tempertureSet = tempertureSet.group(0)

        # 命令を出したユーザ名を取得
        userID = message.channel._client.users[message.body['user']][u'name']

        tdatetime = dt.now()
        if something == "up" or something == "上":
            airconSet.set(hh, mm, tempertureSet, "up")
            message.reply("時刻" + timeSet + "に" + tempertureSet + "℃上げるようにセットしました。")
        elif something == "down" or something == "下":
            airconSet.set(hh, mm, tempertureSet, "down")
            message.reply("時刻" + timeSet + "に" + tempertureSet + "℃下げるようにセットしました。")
        print(tdatetime, "accept oder from ", userID, )
    except Exception as e:
        print(e)
        message.reply("タイマーセットの入力書式は hhmm temp up/down です")


@listen_to(u'(reset|リセット|削除|delete)+')
@respond_to(u'(reset|リセット|削除|delete)+')
def timerReset(message, something):
    try:
        text = message.body['text']
        airconSet.timer_remove()
        message.reply("タイマー設定を削除しました。")
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


@listen_to(u'(setting|設定)+')
@respond_to(u'(setting|設定)+')
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
            "今すぐ→now on/off/up/down ただしonとoffは区別できません, タイマーセット→ hhmm temp up/down。　タイマー設定の削除→ リセット、タイマースタート→ スタート。設定時刻確認→ 設定。動き出したタイマーを止めるにはストップボタンを押してください。")
    except Exception as e:
        print(e)
        message.reply("指示を解釈できませんでした。")

