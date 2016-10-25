# -*- coding: utf-8 -*-

from kivy.lib import osc
from kivy.clock import Clock
from kivy.storage.dictstore import DictStore

from time import sleep

from plyer import notification, vibrator

from os.path import join
from time import time

import paramiko

class PXPAppService():
  def __init__(self):
    self.path = ''
    self.passwd = ''
    self.directories = [
      'Home',
      'Tees',
      'SweatNHoodies',
      'Shirts',
      'Jackets',
      'Coats',
      'Sweaters',
      'Denim',
      'Jogging',
      'Pants',
      'Sneakers',
      'Accessories',
      'NewIn',
      'Sales']
    self.images_names = {}
  
  def get_info(self, *args):
    if str(args[0][2]) == 'path and passwd':
      self.path = str(args[0][3])
      self.passwd = str(args[0][4])
      vibrator.vibrate(0.5)
  
  # execute a command on the server
  # time consuming operation, should be done the least
  def exec_command(self, cmd):
    client = paramiko.client.SSHClient()
    client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
    client.connect(
      '178.170.72.68',
      port = 44700,
      username = 'pierre',
      password = self.passwd)
    stdin, stdout, stderr = client.exec_command(cmd)
    output = []
    for line in stdout.readlines():
      output.append(str(line))
    client.close()
    return output
  
  def update_names(self):
    directory = '/var/www/PXPAppProducts/'
    print 'not implemented yet'
  
  def update_infos(self):
    directory = '/home/pierre/PXPAppProducts/'
    print 'not implemented yet'
  
  def update_notif(self):
    print 'not implemented yet'
  
  def update_all(self):
    self.update_names()
    self.update_infos()
    self.update_notif()

def send_msg(message):
  if message == 'passwd':
    osc.sendMsg('/app-path', ['not implemented loul', ], port=3002)

# get the application time stamp from last notification
def get_last_stamp(path):
  store = DictStore(path)
  LS = None
  if store.exists('last_stamp'):
    LS = store.get('last_stamp')['sec']
  else:
    LS = str(time())
    store.put('last_stamp', sec = LS)
  return LS

# retrieve the list of stamps from the server
def get_server_stamp(LS):
  return 'not implemented yet'

if __name__ == '__main__':
  
  pxp = PXPAppService()
  
  osc.init()
  oscid = osc.listen(ipAddr='0.0.0.0', port=3000)
  osc.bind(oscid, pxp.get_info, '/service-info')
  
  # waiting for the password and notification path to be sent
  while not (pxp.path and pxp.passwd):
    osc.readQueue(oscid)
    sleep(.1)
  
  # main loop
  # get the time-critical content up-to-date for the app
  #   - images names
  #   - references and prices
  # sleep value should be set to 300 for release not to consume too much bandwidth
  while True:
    notification.notify(title='service', message='starts to update like a bitch')
    pxp.update_all()
    sleep(10)




