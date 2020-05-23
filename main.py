# -*- coding: utf-8 -*-
import slackBot
import bme280
import datetime as dt
import threading


def worker1():
    slackBot.main()


def worker2():
    bme280.get_env_loop()


if __name__ == "__main__":
    print("Main Start!")
    t1 = threading.Thread(target=worker1)
    t2 = threading.Thread(target=worker2)
    t1.start()
    t2.start()
