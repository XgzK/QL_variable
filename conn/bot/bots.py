"""
TG机器人
"""
from telebot import asyncio_helper, TeleBot

from conn.gheaders.conn import read_yaml


class Bot:
    def __init__(self):
        yml = read_yaml()
        self.token = yml['Token']
        self.bots = TeleBot(self.token)
        asyncio_helper.proxy = yml['Proxy']
        self.chat_id = []  # 群组和频道
        self.status = ["left", "member", "administrator", "creator"]  # member 成员 left 不在群组 administrator 管理员 creator 群主
