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
    self.directories = []
    self.images_names = {}
  
  def get_info(self, *args):
    if str(args[0][2]) == 'path and passwd':
      self.path = str(args[0][3])
      self.passwd = str(args[0][4])
      vibrator.vibrate(0.5)
  
  def send_info(self):
    for dir in self.images_names.keys():
      data = [dir]
      for image in self.images_names[dir]:
        data.append(image)
      osc.sendMsg('/app-info', data, port=3002)
      sleep(1)
  
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
      output.append(str(line).split('\n')[0])
    client.close()
    return output
  
  def update_names(self):
    output = self.exec_command('ls -R /var/www/PXPAppProducts/')
    current_dir = ''
    for entry in output:
      pathname = entry.split('/')
      image_name = entry.split('.')
      if len(pathname) == 5 and pathname[4] != ':':
        current_dir = pathname[4].split(':')[0]
        self.directories.append(current_dir)
        self.images_names[current_dir] = []
      elif len(image_name) == 2 and image_name[1] == 'jpg':
        self.images_names[current_dir].append(entry)
  
  def update_infos(self):
    directory = '/home/pierre/PXPAppProducts/'
    print 'not implemented yet'
  
  def update_notif(self):
    print 'not implemented yet'
  
  def update_all(self):
    self.update_names()
    self.update_infos()
    self.update_notif()

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
    pxp.update_all()
    pxp.send_info()
    sleep(1)




