# -*- coding: utf-8 -*-
import time
import datetime
import re
from datetime import datetime as dt
import wiringpi


# OUTPUT
PIN_UP = 23  # BCM No
PIN_DOWN = 24
PIN_POWER = 25
PIN_RESET = 15

# GPIO初期化
wiringpi.wiringPiSetupGpio()
# GPIOを入力モード（0）/出力モード(1)に設定
wiringpi.pinMode(PIN_UP, 1)
wiringpi.pinMode(PIN_DOWN, 1)
wiringpi.pinMode(PIN_POWER, 1)
wiringpi.digitalWrite(PIN_RESET, 0)

# 出力をLow
wiringpi.digitalWrite(PIN_UP, 0)
wiringpi.digitalWrite(PIN_DOWN, 0)
wiringpi.digitalWrite(PIN_POWER, 0)

# ボタン押下時間
wait = 5
onWait = 0.3

print("Aircon set import!")


def timer():
    startTime = datetime.datetime.now().time()
    print(startTime)
    print("タイマースタート")
    file = open('airconTimer.txt', 'r', encoding='utf')
    text = "up"
    try:
        while "up" in text or "down" in text:
            text = file.readline()
            splitText = re.split(" ", text)
            if "up" in text:
                key = 1
            elif "down" in text:
                key = -1
            else:  # キーワードがなければ
                break
            hh = int(splitText[0])
            mm = int(splitText[1])
            tempertureSet = int(splitText[2])
            print("up or down =", str(key), "timer=", str(
                hh), str(mm), "temp=", str(tempertureSet))
    except Exception as e:
        print(e)
    file.close()

    while (wiringpi.digitalRead(PIN_RESET) == 1):  # プルアップしているのでスイッチ押下でLOW
        time.sleep(2)
        tdatetime = dt.now()
        HH = int(tdatetime.strftime('%H'))  # 時刻
        MM = int(tdatetime.strftime('%M'))
        if HH == hh and MM == mm:
            if key == 1:
                aircon_temp_set_up(tempertureSet)
            elif key == -1:
                aircon_temp_set_down(tempertureSet)
            break
    print("タイマーストップ")


def timer_remove():
    file = open('airconTimer.txt', 'w', encoding='utf')
    file.close()


def show_setting():
    print("設定確認")
    file = open('airconTimer.txt', 'r', encoding='utf')
    tmp = "up"
    try:
        while "up" in tmp or "down" in tmp:
            tmp = file.readline()
            if tmp != "":
                text = tmp
    except:
        pass
    print(text)
    return text


def set(hh, mm, number, updown):
    print("Aircon order!")
    print("time= ", hh, mm)
    print("set= ", number)
    file = open('airconTimer.txt', 'a', encoding='utf')  # 追記モードでオープン
    file.write(str(hh)+" "+str(mm)+" "+str(number)+" "+updown+"\n")
    file.close()


def aircon_power():
    print("Aircon power!")
    wiringpi.digitalWrite(PIN_POWER, 1)
    time.sleep(onWait)
    wiringpi.digitalWrite(PIN_POWER, 0)
    time.sleep(wait)


def aircon_temp_set_up(count):
    tdatetime = dt.now()
    print(tdatetime)
    print("aircon_temp_set_up")
    for i in range(count):
        wiringpi.digitalWrite(PIN_UP, 1)
        time.sleep(onWait)
        wiringpi.digitalWrite(PIN_UP, 0)
        time.sleep(wait)
    print("temp set complete!")
    time.sleep(wait)


def aircon_temp_set_down(count):
    tdatetime = dt.now()
    print(tdatetime)
    print("aircon_temp_set_down")
    for i in range(count):
        wiringpi.digitalWrite(PIN_DOWN, 1)
        time.sleep(onWait)
        wiringpi.digitalWrite(PIN_DOWN, 0)
        time.sleep(wait)
    print("temp set complete!")
    time.sleep(wait)


def initialize_GPIO():
    # GPIO初期化
    wiringpi.wiringPiSetupGpio()
    # GPIOを入力モード（0）/出力モード(1)に設定
    wiringpi.pinMode(PIN_UP, 1)
    wiringpi.pinMode(PIN_DOWN, 1)
    wiringpi.pinMode(PIN_POWER, 1)
    wiringpi.digitalWrite(PIN_RESET, 0)
    # 出力をLow
    wiringpi.digitalWrite(PIN_UP, 0)
    wiringpi.digitalWrite(PIN_DOWN, 0)
    wiringpi.digitalWrite(PIN_POWER, 0)


if __name__ == '__main__':
    try:
        time.sleep(1)
        initialize_GPIO()
        # aircon_power()
        # aircon_temp_set_up(3)
        # aircon_temp_set_down(3)
    except Exception as e:
        initialize_GPIO()
        print("----------------------------------")
        print(e)
        print("----------------------------------""\r\n")
