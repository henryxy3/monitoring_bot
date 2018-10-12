"""
Telegram bot monitors the website and sends notifications to chat
"""

# coding: utf-8

import sys
import time
import threading
import requests
from requests.exceptions import ConnectionError
import yaml

CONFIG_FILE = '/etc/samodelkin/samodelkin.yaml'


class MonitoringBot(object):
    """
    Telegram bot
    """

    def __init__(self, token, chat_id, url, str_target):
        """
        Variable initialization
        :type token: string
        :type chat_id: string
        :type url: string
        :type str_target: string
        """
        self.url_api = 'https://api.telegram.org/bot{0}/'.format(token)
        self.chat_id = chat_id
        self.url = url
        self.str_target = str_target
        self.str_not_found = 0
        self.error_network = 0
        self.send_mess_time = time.time()
        self.send_message(self.chat_id, 'Monitoring up')

    def clear_variable(self):
        """
        Clear variables when threading canceled
        """
        self.str_not_found = 0
        self.error_network = 0
        self.send_mess_time = time.time()

    def send_message(self, chat, text):
        """
        Send message to telegram chat
        :type chat: string
        :type text: string
        """
        params = {'chat_id': chat, 'text': text}
        try:
            requests.post(self.url_api + 'sendMessage', data=params)
        except ConnectionError:
            print '[ERROR] api telegram is not available'
            sys.stdout.flush()

    def check_website(self):
        """
        Check answer website
        """
        th_timer = threading.Timer(1, self.check_website)
        th_timer.start()
        try:
            response = requests.get(self.url)
            if self.str_target not in response.content:
                self.str_not_found += 1
        except ConnectionError:
            self.error_network += 1
            print '[ERROR] url is not available'
            sys.stdout.flush()
        if time.time() > self.send_mess_time + 59:
            th_timer.cancel()
            if self.str_not_found != 0 or self.error_network != 0:
                self.send_message(
                    self.chat_id, '{0} is broken. "{1}" not found {2} times '
                    'in the last minute, network error - {3} times'
                    .format(self.url, self.str_target,
                            str(self.str_not_found),
                            str(self.error_network)))
            self.clear_variable()
            self.check_website()

if __name__ == '__main__':
    try:
        with open(CONFIG_FILE) as f:
            CONF = yaml.safe_load(f)
    except EnvironmentError:
        print '[ERROR] config file not loaded'
        sys.stdout.flush()
    try:
        BOT = MonitoringBot(CONF['token'], CONF['chat_id'],
                            CONF['url'], CONF['str_target'])
    except EnvironmentError:
        print '[ERROR] variables not loaded'
        sys.stdout.flush()
    else:
        BOT.check_website()
