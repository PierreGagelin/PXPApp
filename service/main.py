# -*- coding: utf-8 -*-

from kivy.lib import osc
from kivy.clock import Clock

from random import sample, randint
from string import ascii_letters
from time import localtime, asctime, sleep

from plyer import notification, vibrator

from os.path import join
from time import time

received = False

def verify_notification(message, *args):
  pass

def get_path(message, *args):
  received = True

if __name__ == '__main__':
  osc.init()
  oscid = osc.listen(ipAddr='0.0.0.0', port=3000)
  osc.bind(oscid, get_path, '/path')
  Clock.schedule_interval(lambda *x: osc.readQueue(oscid), 0)
  
  # wait for the path to be received
  while not received:
    sleep(0.1)
  
  # notify path reception
  notification.notify(title = 'service', message = 'path received')
  
  # main loop
  while True:
    sleep(10)
