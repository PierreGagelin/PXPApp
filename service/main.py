# -*- coding: utf-8 -*-

from kivy.utils import platform

# does not seems useful as service does not start unless platform is android
#if not platform == 'android':
#  exit()

from plyer import notification
from plyer import vibrator
from time import sleep

if __name__ == '__main__':
  while True:
      notification.notify(
        title= 'Success',
        message= 'notification service active'
      )
      vibrator.vibrate(0.5)
      sleep(30)
