# -*- coding: utf-8 -*-

from kivy.lib import osc
from kivy.clock import Clock
from kivy.storage.dictstore import DictStore

from time import sleep

from plyer import notification, vibrator

from os.path import join
from time import time

# it seems a service has no access to the network :/
import paramiko

class Info():
  def __init__(self):
    self.notification_path = ''
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
  
  def get_info(self, *args):
    if str(args[0][2]) == 'path and passwd':
      self.notification_path = str(args[0][3])
      self.passwd = str(args[0][4])
      vibrator.vibrate(0.5)

def send_msg(message):
  if message == 'passwd':
    osc.sendMsg('/app-path', ['not implemented loul', ], port=3002)

def get_path(*args):
  if str(args[0][2]) == 'path and passwd':
    notification_path = str(args[0][3])
    passwd = str(args[0][4])
    vibrator.vibrate(0.5)
    return [notification_path, passwd]

# execute a command on the server
def exec_command(cmd, passwd):
  client = paramiko.client.SSHClient()
  client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
  client.connect(
    '178.170.72.68',
    port = 44700,
    username = 'pierre',
    password = passwd)
  stdin, stdout, stderr = client.exec_command(cmd)
  output = []
  for line in stdout.readlines():
    output.append(str(line))
  client.close()
  return output

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
  return 'not implemented yet'

if __name__ == '__main__':
  # global information object
  info = Info()
  
  osc.init()
  oscid = osc.listen(ipAddr='0.0.0.0', port=3000)
  osc.bind(oscid, info.get_info, '/service-path')
  
  # main loop
  while True:
    # waiting for the password and notification path to be sent
    if not (info.notification_path and info.passwd):
      osc.readQueue(oscid)
      sleep(.1)
    else:
      LS = get_last_stamp(info.notification_path)
      SS = get_server_stamp(LS)
      ls = exec_command('ls', info.passwd)
      sleep(60)




