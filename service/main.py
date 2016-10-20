# -*- coding: utf-8 -*-

from kivy.utils import platform
from kivy.lib import osc
from kivy.storage.dictstore import DictStore

from plyer import notification
from plyer import vibrator

from os.path import join
from time import time

service = 3000

def some_api_callback(message, *args):
  notification.notify(title = 'WOW', message = str(message))

def verify_notification(message, *args):
  

if __name__ == '__main__':
  osc.init()
  oscid = osc.listen(ipAddr='127.0.0.1', port=service)
  osc.bind(oscid, some_api_callback, '/some_api')
  
  while True:
    osc.readQueue(oscid)
    sleep(.1)
  
  notification.notify(title = 'first', message = 'notification')
  vibrator.vibrate(0.5)
  data_dir = getattr(self, 'user_data_dir')
  store = DictStore(join(data_dir, 'notification.dat'))
  LS = None
  if store.exists('last_stamp'):
	  LS = store.get('last_stamp')['sec']
	else:
	  LS = str(time())
	  store.put('last_stamp', sec = LS)
    ttl = 'title'
    msg = 'last notif: ' + LS
    notification.notify(title = ttl, message = msg)
    vibrator.vibrate(0.5)
    time.sleep(30)





