# -*- coding: utf-8 -*-

# Project X Paris Application (PXPApp) #
########################################
# Multi-platform app: work on Windows, Linux, OS X, Android and iOS
# App for the wholesalers to see products and receive notifications

import kivy
kivy.require('1.9.0')
# to get names more easily
from kivy.app import App
from kivy.app import runTouchApp
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image, AsyncImage
from kivy.graphics import Color, Rectangle
from kivy.graphics import BorderImage
from kivy.core.window import Window
from kivy.utils import platform
from kivy.lang import Builder
from kivy.storage.dictstore import DictStore

# notification system
if not platform == 'ios':
  from plyer import notification

# vibration
if platform == 'android' or platform == 'ios':
  from plyer import vibrator

# to get timestamp for the notifications
from time import time, sleep
from os.path import join

# to retrieve reference and price from a product
#   - ssh with paramiko
#   - personnal socket server
# socket necessary because paramiko won't work on iOS
if not platform == 'ios':
  import paramiko
else:
  import socket

# for some string operations
import string

# to check wholesaler password with salt
import hashlib

# communication between app and service
if platform == 'android':
  from kivy.lib import osc
  from kivy.clock import Clock

# most of the GUI in KV language
design = '''
<HomeBannerWidget>:
  orientation: 'horizontal'
  size_hint: (1, 0.1)
  MenuButton:
    source: 'menu.png'
    size_hint: (0.1, 1)
  Image:
    source: 'empty.png'
    size_hint: (0.9, 1)

<AsyncImageButton>:
  size_hint_y: None
  on_press: self.parent.parent.show_product(self.source)

<ImageButton>:
  size_hint_y: None
  on_press: self.parent.parent.parent.show_product(self.source)

<ImageBannerWidget>:
  orientation: 'horizontal'
  size_hint: (1, 0.1)
  ReturnButton:
    source: 'back.png'
    size_hint: (0.1, 1)
  Image:
    source: 'empty.png'
    size_hint: (0.9, 1)

<GimmeFive>:
  rows: 1
  size_hint: (1, None)
  BoxLayout:
    orientation: 'vertical'
    AsyncImageButton:
      source: 'http://www.projectxparis.com/PXPAppProducts/GF/gf_tl.jpg'
      allow_stretch: True
      size_hint: (1, 0.5)
    AsyncImageButton:
      source: 'http://www.projectxparis.com/PXPAppProducts/GF/gf_bl.jpg'
      allow_stretch: True
      size_hint: (1, 0.5)
  AsyncImageButton:
    source: 'http://www.projectxparis.com/PXPAppProducts/GF/gf_m.jpg'
    allow_stretch: True
    height: 500
  BoxLayout:
    orientation: 'vertical'
    AsyncImageButton:
      source: 'http://www.projectxparis.com/PXPAppProducts/GF/gf_tr.jpg'
      allow_stretch: True
      size_hint: (1, 0.5)
    AsyncImageButton:
      source: 'http://www.projectxparis.com/PXPAppProducts/GF/gf_br.jpg'
      allow_stretch: True
      size_hint: (1, 0.5)

<StoreWidget>:
  cols: 4
  spacing: [2, 4]
  size_hint: (1, None)

<HomeWidget>:
  orientation: 'vertical'
  BodyLayout:
    size_hint: (1, 0.2)
    cols: 1
    Image:
      source: 'banner.jpg'
  HomeBannerWidget:
  ScrollView:
    size_hint: (1, 0.7)
    BodyLayout:
      cols: 1
      size_hint_y: None
      height: self.minimum_height
      GimmeFive:
      StoreWidget:
        id: store

<MenuWidget>:
  orientation: 'vertical'
  ImageBannerWidget:
  ScrollView:
    size_hint: (1, 0.9)
    BodyLayout:
      cols: 1
      size_hint_y: None
      height: self.minimum_height
      CategoriesButton:
      NewInButton:
      SalesButton:
      ContactButton:

<CategoriesButton>:
  size_hint: (1, None)
  text: 'Categories'
  on_press: self.parent.parent.parent.show_categories()

<CategoriesButtons>:
  size_hint: (1, None)
  cols: 2
  Image:
    size_hint: (0.2, None)
    source: 'empty.png'
  Button:
    size_hint: (0.8, None)
    text: 'Tees'
    on_press: root.parent.parent.parent.show_category('Tees')
  Image:
    size_hint: (0.2, None)
    source: 'empty.png'
  Button:
    size_hint: (0.8, None)
    text: 'Sweat & Hoodies'
    on_press: root.parent.parent.parent.show_category('SweatNHoodies')
  Image:
    size_hint: (0.2, None)
    source: 'empty.png'
  Button:
    size_hint: (0.8, None)
    text: 'Shirts'
    on_press: root.parent.parent.parent.show_category('Shirts')
  Image:
    size_hint: (0.2, None)
    source: 'empty.png'
  Button:
    size_hint: (0.8, None)
    text: 'Jackets'
    on_press: root.parent.parent.parent.show_category('Jackets')
  Image:
    size_hint: (0.2, None)
    source: 'empty.png'
  Button:
    size_hint: (0.8, None)
    text: 'Coats'
    on_press: root.parent.parent.parent.show_category('Coats')
  Image:
    size_hint: (0.2, None)
    source: 'empty.png'
  Button:
    size_hint: (0.8, None)
    text: 'Sweaters'
    on_press: root.parent.parent.parent.show_category('Sweaters')
  Image:
    size_hint: (0.2, None)
    source: 'empty.png'
  Button:
    size_hint: (0.8, None)
    text: 'Denim'
    on_press: root.parent.parent.parent.show_category('Denim')
  Image:
    size_hint: (0.2, None)
    source: 'empty.png'
  Button:
    size_hint: (0.8, None)
    text: 'Jogging'
    on_press: root.parent.parent.parent.show_category('Jogging')
  Image:
    size_hint: (0.2, None)
    source: 'empty.png'
  Button:
    size_hint: (0.8, None)
    text: 'Pants'
    on_press: root.parent.parent.parent.show_category('Pants')
  Image:
    size_hint: (0.2, None)
    source: 'empty.png'
  Button:
    size_hint: (0.8, None)
    text: 'Sneakers'
    on_press: root.parent.parent.parent.show_category('Sneakers')
  Image:
    size_hint: (0.2, None)
    source: 'empty.png'
  Button:
    size_hint: (0.8, None)
    text: 'Accessories'
    on_press: root.parent.parent.parent.show_category('Accessories')

<NewInButton>:
  size_hint: (1, None)
  text: 'New In'
  on_press: self.parent.parent.parent.show_category('NewIn')

<SalesButton>:
  size_hint: (1, None)
  text: 'Sales'
  on_press: self.parent.parent.parent.show_category('Sales')

<ContactButton>:
  size_hint: (1, None)
  text: 'Contact'
  on_press: self.parent.parent.parent.show_contact()

<ProductWidget>:
  orientation: 'vertical'
  ImageBannerWidget:
  Label:
    id: product_reference
    size_hint: (1, 0.05)
    text: 'reference not loaded yet'
  AsyncImage:
    id: product_image
    size_hint: (1, 0.6)
  BoxLayout:
    orientation: 'horizontal'
    size_hint: (1, 0.2)
    ProductImage:
      id: product_image0
      on_press: root.switch_image(self.source)
    ProductImage:
      id: product_image1
      on_press: root.switch_image(self.source)
    ProductImage:
      id: product_image2
      on_press: root.switch_image(self.source)
  Label:
    id: product_price
    size_hint: (1, 0.05)
    text: 'price not loaded yet'

<CategoryWidget>:
  orientation: 'vertical'
  BodyLayout:
    size_hint: (1, 0.2)
    cols: 1
    Image:
      source: 'banner.jpg'
  ImageBannerWidget:
  ScrollView:
    size_hint: (1, 0.7)
    BodyLayout:
      id: category_grid
      cols: 4
      size_hint_y: None
      height: self.minimum_height

<AuthenticationWidget>:
  orientation: 'vertical'
  Label:
    id: failure
  BoxLayout:
    orientation: 'horizontal'
    Label:
      text: 'Mot de passe : '
    TextInput:
      id: attempt
      password: True
      text: ''
  Button:
    text: 'Connecter'
    on_press: root.validate()
'''

# builds GUI
Builder.load_string(design)

# authenticate the wholesaler with his password
class AuthenticationWidget(BoxLayout):
  def __init__(self, **kwargs):
    super(AuthenticationWidget, self).__init__(**kwargs)
  
  def validate(self):
    if hashlib.sha256(self.ids['attempt'].text).hexdigest() == self.parent.salt:
      self.parent.passwd = self.ids['attempt'].text
      app.send_info()
      self.clear_widgets()
      self.parent.__clear__()
    else:
      self.ids['failure'].text = 'Mot de passe erroné, essayez à nouveau'
      self.ids['attempt'].text = ''

class ReturnButton(ButtonBehavior, Image):
  def __init__(self, **kwargs):
    super(ReturnButton, self).__init__(**kwargs)
  
  def on_press(self):
    self.parent.parent.return_to_root()

class HomeButton(ButtonBehavior, Image):
  def __init__(self, **kwargs):
    super(HomeButton, self).__init__(**kwargs)
  
  def on_press(self):
    self.parent.parent.__init__()

class MenuButton(ButtonBehavior, Image):
  def __init__(self, **kwargs):
    super(MenuButton, self).__init__(**kwargs)
  
  def on_press(self):
    self.parent.parent.parent.show_menu()

class AsyncImageButton(ButtonBehavior, AsyncImage):
  pass

class ImageButton(ButtonBehavior, Image):
  pass

class BannerLayout(BoxLayout):
  def __init__(self, **kwargs):
    super(BannerLayout, self).__init__(**kwargs)
    
    with self.canvas.before:
        Color(0, 0, 0, 0.8)
        self.rect = Rectangle(size=self.size, pos=self.pos)
    # follow size and position updates
    self.bind(size=self._update_rect, pos=self._update_rect)
  
  def _update_rect(self, instance, value):
    self.rect.pos = instance.pos
    self.rect.size = instance.size

class BodyLayout(GridLayout):
  def __init__(self, **kwargs):
    super(BodyLayout, self).__init__(**kwargs)
    
    with self.canvas.before:
        Color(1, 1, 1, 1)
        self.rect = Rectangle(size=self.size, pos=self.pos)
    # follow size and position updates
    self.bind(size=self._update_rect, pos=self._update_rect)
  
  def _update_rect(self, instance, value):
    self.rect.pos = instance.pos
    self.rect.size = instance.size
  
  def show_product(self, source):
    self.parent.parent.show_product(source)

class ImageBannerWidget(BannerLayout):
  pass

class HomeBannerWidget(BannerLayout):
  pass

class GimmeFive(GridLayout):
  def __init__(self, **kwargs):
    super(GimmeFive, self).__init__(**kwargs)
    self.bind(minimum_height=self.setter('height'))
  
  def show_product(self, source_add):
    self.parent.show_product(source_add)

class StoreWidget(BodyLayout):
  def __init__(self, **kwargs):
    super(StoreWidget, self).__init__(**kwargs)
    # for the ScrollView
    self.bind(minimum_height=self.setter('height'))
    # loading images
    #self.load_images()
  
  # sending message via the socket
  def send_msg(self, cs, msg):
    sntlen = 0
    ttllen = len(msg)
    while sntlen < ttllen:
      snt = cs.send(msg[sntlen:])
      if snt == 0:
        raise RuntimeError('socket broken')
      sntlen += snt
  
  # receiving message from the socket
  #  - msglen is the hard part
  def rcvd_msg(self, cs, msglen):
    chunks = []
    bytrcv = 0
    while bytrcv < msglen:
      print 'waiting a chunk...'
      chunk = cs.recv(min(msglen - bytrcv, 2048))
      if chunk == '':
        raise RuntimeError('socket broken')
      chunks.append(chunk)
      bytrcv += len(chunk)
    return ''.join(chunks)
  
  # loading images from "Home" directory
  def load_images(self):
    images = []
    cmd = 'ls /var/www/PXPAppProducts/Home/'
    # filling images with data from the server
    if platform == 'android':
      # updating image with app.images_names['Home']
      if app.images_names.has_key('Home'):
        for image in app.images_names['Home']:
          image = image.split('_')[0]
          if not image in images:
            images.append(image)
    elif not platform == "ios":
      client = paramiko.client.SSHClient()
      client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
      client.connect(
        '178.170.72.68',
        port = 44700,
        username = 'pierre',
        password = self.parent.parent.parent.parent.passwd)
      stdin, stdout, stderr = client.exec_command(cmd)
      for entry in stdout.readlines():
        entry = str(entry).split('\n')[0]
        info = entry.split('.')
        if len(info) == 2 and info[1] == 'jpg':
          entry = entry.split('_')[0]
          if not(entry in images):
            images.append(entry)
      client.close()
    else:
      # retrieve same information for iOS
      # this is low-level networking... some things are weird:
      #   - size does matter (e.g. cmd shall not be more than 10^256 char)
      #   - same for command's result
      cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      cs.connect(('127.0.0.1', 2016))
      cmdlen = len(cmd)
      if len(str(cmdlen)) > 256:
        print 'load_images: error: command too long'
        return
      socket_cmd_size = '0'*(256-len(str(cmdlen))) + str(cmdlen)
      self.send_msg(cs, socket_cmd_size)
      self.send_msg(cs, cmd)
      res_size = self.rcvd_msg(cs, 256)
      reslen = int(res_size)
      res = self.rcvd_msg(cs, reslen)
      for entry in res.split('\n'):
        print 'entry: ', entry
        info = entry.split('.')
        if len(info) == 2 and info[1] == 'jpg':
          entry = entry.split('_')[0]
          if not(entry in images):
            images.append(entry)
    # retrieving images via URL and add it to the app
    for image in images:
      image += '_0.jpg'
      src = 'http://www.projectxparis.com/PXPAppProducts/Home/'+ image
      self.add_widget(AsyncImageButton(
        source = src,
        allow_stretch = True,
        size_hint = (1, None),
        height = 200))

class ProductImage(ButtonBehavior, AsyncImage):
  def __init__(self, **kwargs):
    super(ProductImage, self).__init__(**kwargs)

class HomeWidget(BoxLayout):
  def __init__(self, **kwargs):
    self.clear_widgets()
    super(HomeWidget, self).__init__(**kwargs)
  
  def show_product(self, product_source):
    self.clear_widgets()
    self.parent.show_product(product_source)

class MenuWidget(BoxLayout):
  def __init__(self, **kwargs):
    self.clear_widgets()
    self.is_categories = False
    super(MenuWidget, self).__init__(**kwargs)
  
  def return_to_root(self):
    self.clear_widgets()
    self.is_categories = False
    self.parent.__clear__()
  
  def show_categories(self):
    # clear widgets
    self.children[0].children[0].clear_widgets()
    # organize the menu
    if self.is_categories:
      self.is_categories = False
      self.children[0].children[0].add_widget(CategoriesButton())
      self.children[0].children[0].add_widget(NewInButton())
      self.children[0].children[0].add_widget(SalesButton())
      self.children[0].children[0].add_widget(ContactButton())
    else:
      self.is_categories = True
      self.children[0].children[0].add_widget(CategoriesButton())
      self.children[0].children[0].add_widget(CategoriesButtons())
      self.children[0].children[0].add_widget(NewInButton())
      self.children[0].children[0].add_widget(SalesButton())
      self.children[0].children[0].add_widget(ContactButton())
  
  def show_category(self, category):
    self.clear_widgets()
    self.is_categories = False
    self.parent.show_category(category)
  
  def show_contact(self):
    pass

class CategoryWidget(BoxLayout):
  def __init__(self, **kwargs):
    self.clear_widgets()
    super(CategoryWidget, self).__init__(**kwargs)
  
  # sending message via the socket
  def send_msg(self, cs, msg):
    sntlen = 0
    ttllen = len(msg)
    while sntlen < ttllen:
      snt = cs.send(msg[sntlen:])
      if snt == 0:
        raise RuntimeError('socket broken')
      sntlen += snt
  
  # receiving message from the socket
  #  - msglen is the hard part
  def rcvd_msg(self, cs, msglen):
    chunks = []
    bytrcv = 0
    while bytrcv < msglen:
      print 'waiting a chunk...'
      chunk = cs.recv(min(msglen - bytrcv, 2048))
      if chunk == '':
        raise RuntimeError('socket broken')
      chunks.append(chunk)
      bytrcv += len(chunk)
    return ''.join(chunks)
  
  def update(self, directory):
    cmd = 'ls /var/www/PXPAppProducts/' + directory + '/'
    images = []
    # filling images with data from the server
    if platform == 'android':
      # updating image with app.images_names[directory]
      if app.images_names.has_key(directory):
        for image in app.images_names[directory]:
          image = image.split('_')[0]
          if not image in images:
            images.append(image)
    elif not platform == 'ios':
      client = paramiko.client.SSHClient()
      client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
      client.connect(
        '178.170.72.68',
        port = 44700,
        username = 'pierre',
        password = self.parent.passwd)
      stdin, stdout, stderr = client.exec_command(cmd)
      for entry in stdout.readlines():
        entry = str(entry).split('\n')[0]
        info = entry.split('.')
        if len(info) == 2 and info[1] == 'jpg':
          entry = entry.split('_')[0]
          if not(entry in images):
            images.append(entry)
      client.close()
    else:
      # retrieve same information for iOS
      # this is low-level networking... some things are weird:
      #   - size does matter (e.g. cmd shall not be more than 10^256 char)
      #   - same for command's result
      cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      cs.connect(('127.0.0.1', 2016))
      cmdlen = len(cmd)
      if len(str(cmdlen)) > 256:
        print 'load_images: error: command too long'
        return
      socket_cmd_size = '0'*(256-len(str(cmdlen))) + str(cmdlen)
      self.send_msg(cs, socket_cmd_size)
      self.send_msg(cs, cmd)
      res_size = self.rcvd_msg(cs, 256)
      reslen = int(res_size)
      res = self.rcvd_msg(cs, reslen)
      for entry in res.split('\n'):
        print 'entry: ', entry
        info = entry.split('.')
        if len(info) == 2 and info[1] == 'jpg':
          entry = entry.split('_')[0]
          if not(entry in images):
            images.append(entry)
    for image in images:
      image += '_0.jpg'
      src = 'http://www.projectxparis.com/PXPAppProducts/'+ directory + '/' + image
      self.add_widget(AsyncImageButton(
        source = src,
        allow_stretch = True,
        size_hint = (1, None),
        height = 200))
  
  def return_to_root(self):
    self.clear_widgets()
    self.parent.return_to_root()

class CategoriesButton(Button):
  pass

class CategoriesButtons(GridLayout):
  def __init__(self, **kwargs):
    super(CategoriesButtons, self).__init__(**kwargs)
    # for the ScrollView
    self.bind(minimum_height=self.setter('height'))

class NewInButton(Button):
  pass

class SalesButton(Button):
  pass

class ContactButton(Button):
  pass

class ProductWidget(BoxLayout):
  def __init__(self, **kwargs):
    self.clear_widgets()
    super(ProductWidget, self).__init__(**kwargs)
  
  # sending message via the socket
  def send_msg(self, cs, msg):
    sntlen = 0
    ttllen = len(msg)
    while sntlen < ttllen:
      snt = cs.send(msg[sntlen:])
      if snt == 0:
        raise RuntimeError('socket broken')
      sntlen += snt
  
  # receiving message from the socket
  #  - msglen is the hard part
  def rcvd_msg(self, cs, msglen):
    chunks = []
    bytrcv = 0
    while bytrcv < msglen:
      print 'waiting a chunk...'
      chunk = cs.recv(min(msglen - bytrcv, 2048))
      if chunk == '':
        raise RuntimeError('socket broken')
      chunks.append(chunk)
      bytrcv += len(chunk)
    return ''.join(chunks)
  
  def update(self, source_add):
    source1 = string.replace(source_add, '_0.jpg', '_1.jpg')
    source2 = string.replace(source_add, '_0.jpg', '_2.jpg')
    self.ids['product_image'].source = source_add
    self.ids['product_image0'].source = source_add
    self.ids['product_image1'].source = source1
    self.ids['product_image2'].source = source2
    directory = source_add.split('/')[len(source_add.split('/'))-2]
    name = source_add.split('/')[len(source_add.split('/'))-1]
    name = name.split('_')[0]
    ref_cmd = 'cat /home/pierre/PXPAppProducts/' + directory + '/' + \
      name + '_ref.txt'
    price_cmd = string.replace(ref_cmd, '_ref.txt', '_price.txt')
    if platform == 'android':
      if app.images_infos.has_key(directory):
        for dic in app.images_infos[directory]:
          if dic['name'] == name and dic['type'] == 'price':
            self.ids['product_price'].text = dic['value']
          elif dic['name'] == name and dic['type'] == 'ref':
            self.ids['product_reference'].text = dic['value']
    elif not platform == 'ios':
     if False:
      client = paramiko.client.SSHClient()
      client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
      client.connect(
        '178.170.72.68',
        port = 44700,
        username = 'pierre',
        password = self.parent.passwd)
      stdin, stdout, stderr = client.exec_command(ref_cmd)
      for ref in stdout.readlines():
        self.ids['product_reference'].text = 'référence : ' + \
          str(ref).split('\n')[0]
      stdin, stdout, stderr = client.exec_command(price_cmd)
      for price in stdout.readlines():
        self.ids['product_price'].text = str(price).split('\n')[0] + '€'
      client.close()
     else:
      # we update informations according to app.images_infos
      print 'not implemented yet'
    else:
      # retrieve same information for iOS
      # this is low-level networking... some things are weird:
      #   - size does matter (e.g. cmd shall not be more than 10^256 char)
      #   - same for command's result
      cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      cs.connect(('127.0.0.1', 2016))
      cmdlen = len(ref_cmd)
      if len(str(cmdlen)) > 256:
        print 'load_images: error: command too long'
        return
      socket_cmd_size = '0'*(256-len(str(cmdlen))) + str(cmdlen)
      self.send_msg(cs, socket_cmd_size)
      self.send_msg(cs, ref_cmd)
      res_size = self.rcvd_msg(cs, 256)
      reslen = int(res_size)
      res = self.rcvd_msg(cs, reslen)
      self.ids['product_reference'].text = 'référence : ' + \
        str(res).split('\n')[0]
      cs.close()
      # we just got the ref, now  same for the price
      cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      cs.connect(('127.0.0.1', 2016))
      cmdlen = len(price_cmd)
      if len(str(cmdlen)) > 256:
        print 'load_images: error: command too long'
        return
      socket_cmd_size = '0'*(256-len(str(cmdlen))) + str(cmdlen)
      self.send_msg(cs, socket_cmd_size)
      self.send_msg(cs, price_cmd)
      res_size = self.rcvd_msg(cs, 256)
      reslen = int(res_size)
      res = self.rcvd_msg(cs, reslen)
      self.ids['product_price'].text = str(res).split('\n')[0] + '€'
      cs.close()
  
  def switch_image(self, source_add):
    self.ids['product_image'].source = source_add
  
  def return_to_root(self):
    self.clear_widgets()
    self.parent.__clear__()

# main widget, responsible of switching between views
# should use Factory in order to cache memory (is slow otherwise)
class RootWidget(BoxLayout):
  salt = '97fde7b312f0d79dbadaeb0c63fd270c9a168ea4a21f060d8cb9bf9000df905d'
  passwd = None
  def __init__(self, **kwargs):
    super(RootWidget, self).__init__(**kwargs)
    # authenticate the wholesaler to the app
    self.clear_widgets()
    self.authenticate()
  
  # clear widgets and starts again with authentication
  def __clear__(self):
    self.clear_widgets()
    self.authenticate()
  
  # authenticate the user as a wholesaler
  def authenticate(self):
    if self.passwd:
      HW = HomeWidget()
      self.add_widget(HW)
      HW.ids['store'].load_images()
    else:
      self.clear_widgets()
      self.add_widget(AuthenticationWidget())
  
  # initialize again
  def return_to_root(self):
    self.__clear__()
  
  # show the menu
  def show_menu(self):
    self.clear_widgets()
    self.add_widget(MenuWidget())
  
  # show subcategories from the menu
  def show_category(self, category):
    self.clear_widgets()
    CW = CategoryWidget()
    self.add_widget(CW)
    CW.update(category)
  
  # show the product view
  def show_product(self, source_add):
    self.clear_widgets()
    PW = ProductWidget()
    self.add_widget(PW)
    PW.update(source_add)

class PXPApp(App):
  def build(self):
    self.images_names = {}
    self.images_infos = {}
    
    # launch the notification service
    # setup the OSC communication
    if platform == 'android':
      from android import AndroidService
      service = AndroidService(
        'hello',
        'world')
      service.start('useless')
      self.service = service
      osc.init()
      oscid = osc.listen(port=3002)
      osc.bind(oscid, self.get_info, '/app-info')
      Clock.schedule_interval(lambda *x: osc.readQueue(oscid), 0)
    
    self.root = RootWidget()
    return self.root
  
  # reception of service information
  def get_info(self, *args):
    if args[0][2] == 'names':
      self.images_names[args[0][3]] = []
      for image in args[0][4:]:
        self.images_names[args[0][3]].append(image)
    elif args[0][2] == 'infos':
      self.images_infos[args[0][3]] = []
      for entry in args[0][4:]:
        dic = {}
        for key in entry.split(';'):
          dic[key.split(':')[0]] = key.split(':')[1]
        self.images_infos[args[0][3]].append(dic)
  
  # send the path where the timestamp file is
  def send_info(self, *args):
    if platform == 'android':
      data_dir = getattr(self, 'user_data_dir')
      path = join(data_dir, 'notification.dat')
      osc.sendMsg('/service-info', ['path and passwd', path, self.root.passwd, ], port=3000)
  
  # so that memory is kept when app is left but not killed
  def on_pause(self):
    return True

app = PXPApp()
if __name__ == '__main__':
  app.run()




