# -*- coding: utf-8 -*-

from kivy.lib import osc
from kivy.clock import Clock
from kivy.storage.dictstore import DictStore

from time import sleep

from plyer import notification, vibrator

from os.path import join
from time import time

# import paramiko

notification_path = ''
passwd = ''

def send_msg():
  osc.sendMsg('/app-path', ['coucou', ], port=3002)

def get_path(*args):
  notification_path = str(args[0][2])
  passwd = str(args[0][3])
  # notification.notify(title = 'service', message = 'message: ' + passwd)
  vibrator.vibrate(0.5)
  osc.sendMsg('/app-path', ['coucoudepath', ], port = 3002)

# get the application time stamp from last notification
def get_last_stamp(notification_path):
  store = DictStore(notification_path)
  LS = None
  if store.exists('last_stamp'):
    LS = store.get('last_stamp')['sec']
  else:
    LS = str(time())
    store.put('last_stamp', sec = LS)
  return LS

# retrieve the list of stamps from the server
def get_server_stamp(LS):
  print 'not implemented yet'

if __name__ == '__main__':
  osc.init()
  oscid = osc.listen(ipAddr='0.0.0.0', port=3000)
  osc.bind(oscid, get_path, '/service-path')
  
  # main loop
  while True:
    if not (notification_path and passwd):
      osc.readQueue(oscid)
      send_msg()
      sleep(.1)
    else:
      LS = get_last_stamp(notification_path)
      SS = get_server_stamp(LS)
      sleep(60)




