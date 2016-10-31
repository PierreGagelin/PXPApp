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
    self.images_names = {}
    self.images_infos = {}
    self.LS = 0
  
  def get_info(self, *args):
    if str(args[0][2]) == 'path and passwd':
      self.path = str(args[0][3])
      self.passwd = str(args[0][4])
      vibrator.vibrate(0.5)
  
  def send_names(self):
    print 'begin to send names...'
    for dir in self.images_names.keys():
      data = ['names', dir]
      for image in self.images_names[dir]:
        data.append(image)
      osc.sendMsg('/app-info', data, port=3002)
    print '...names sent'
  
  def send_infos(self):
    print 'begin to send infos...'
    for dir in self.images_infos.keys():
      data = ['infos', dir]
      for dic in self.images_infos[dir]:
        data.append('name:'+dic['name']+';type:'+dic['type']+';value:'+dic['value'])
      osc.sendMsg('/app-info', data, port=3002)
    print '...infos sent'
  
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
    print 'begin to update names...'
    output = self.exec_command('ls -R /var/www/PXPAppProducts/')
    current_dir = ''
    for entry in output:
      pathname = entry.split('/')
      image_name = entry.split('.')
      if len(pathname) == 5 and pathname[4] != ':':
        current_dir = pathname[4].split(':')[0]
        self.images_names[current_dir] = []
      elif len(image_name) == 2 and image_name[1] == 'jpg':
        self.images_names[current_dir].append(entry)
    print '...names updated'
  
  def update_infos(self):
    print 'begin to update infos...'
    output = self.exec_command('ls -R /home/pierre/PXPAppProducts/')
    current_dir = ''
    for entry in output:
      pathname = entry.split('/')
      image_info = entry.split('.')
      if len(pathname) == 5 and pathname[4] != ':':
        current_dir = pathname[4].split(':')[0]
        self.images_infos[current_dir] = []
      elif len(image_info) == 2 and image_info[1] == 'txt':
        info = image_info[0].split('_')
        if len(info) == 3:
          dic = {'name': info[0], 'type': info[1], 'value': info[2]}
          self.images_infos[current_dir].append(dic)
        else:
          # consider adding a log file to list issues
          print 'corrupted entry found!'
    print '...infos updated'
  
  def update_notif(self):
    print 'begin to update notif...'
    # the command is ordered by modification time so only the first output is interessant
    name = self.exec_command('ls -c /home/pierre/notifications')[0]
    stamp = self.exec_command('stat -c %Y /home/pierre/notifications/' + name)
    print 'name: ', name
    print 'stamp: ', stamp
    notif = {'name': name, 'stamp': stamp}
    print 'most recent notif: ', notif
    if notif['stamp'] > self.LS:
      print 'gonna set_last_stamp and send notification'
    print '...notif updated'
  
  def update_all(self):
    self.update_names()
    self.update_infos()
    self.update_notif()
  
  def init_last_stamp(self):
    store = DictStore(self.path)
    if store.exists('last_stamp'):
      self.LS = store.get('last_stamp')['sec']
    else:
      self.LS = int(time())
      store.put('last_stamp', sec = self.LS)
  
  def set_last_stamp(self, stamp):
    store = DictStore(self.path)
    store.put('last_stamp', sec = stamp)
    self.LS = stamp

if __name__ == '__main__':
  
  pxp = PXPAppService()
  
  osc.init()
  oscid = osc.listen(ipAddr='0.0.0.0', port=3000)
  osc.bind(oscid, pxp.get_info, '/service-info')
  
  # waiting for the password and notification path to be sent
  while not (pxp.path and pxp.passwd):
    osc.readQueue(oscid)
    sleep(.1)
  
  # initialize the stamp value
  pxp.init_last_stamp()
  
  # main loop
  # get the time-critical content up-to-date for the app
  #   - images names
  #   - references and prices
  # sleep value should be set to 300 for release not to consume too much bandwidth
  while True:
    pxp.update_all()
    pxp.send_names()
    pxp.send_infos()
    sleep(10)




