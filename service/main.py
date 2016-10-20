# -*- coding: utf-8 -*-

from kivy.lib import osc
from kivy.clock import Clock

from time import sleep

from plyer import notification, vibrator

from os.path import join
from time import time

def send_msg():
  osc.sendMsg('/app-path', ['coucou', ], port=3002)

def get_path(*args):
  notification.notify(title = 'service', message = 'got message')
  vibrator.vibrate(0.5)
  osc.sendMsg('/app-path', ['coucoudepath', ], port = 3002)

if __name__ == '__main__':
  osc.init()
  oscid = osc.listen(ipAddr='0.0.0.0', port=3000)
  osc.bind(oscid, get_path, '/service-path')
  # Clock.schedule_interval(lambda *x: osc.readQueue(oscid), 0)
  
  # main loop
  while True:
    osc.readQueue(oscid)
    send_msg()
    sleep(.1)




