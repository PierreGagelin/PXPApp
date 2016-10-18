# -*- coding: utf-8 -*-

from kivy.lib import osc
from kivy.clock import Clock
from random import sample, randint
from string import ascii_letters
from time import localtime, asctime, sleep

from plyer import notification, vibrator

def ping(*args):
  notification.notify(title = 'service', message = 'ping')
  vibrator.vibrate(0.5)
  osc.sendMsg(
    '/message',
    [''.join(sample(ascii_letters, randint(10, 20))), ],
    port=3002)

def send_date():
  osc.sendMsg('/date', [asctime(localtime()), ], port=3002)

if __name__ == '__main__':
  osc.init()
  oscid = osc.listen(ipAddr='0.0.0.0', port=3000)
  osc.bind(oscid, ping, '/ping')
  Clock.schedule_interval(lambda *x: osc.readQueue(oscid), 0)
  while True:
    osc.readQueue(oscid)
    sleep(5)
