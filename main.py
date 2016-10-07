# -*- coding: utf-8 -*-

import kivy
kivy.require('1.9.1') # current kivy version

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

# plyer should work on iOS but not for notification
if platform == "android":
  from plyer import notification
else:
  notification = None
try:
  from plyer import vibrator
except:
  vibrator = None

from kivy.clock import Clock, mainthread
import threading
import time

import paramiko, socket

import string

import hashlib

from kivy.lang import Builder

design = '''
<HomeBannerWidget>:
  orientation: 'horizontal'
  size_hint: (1, 0.1)
  MenuButton:
    source: 'menu.png'
    size_hint: (0.1, 1)
  Image:
    source: 'empty.png'
    size_hint: (0.4, 1)
  PXPLogo:
    size_hint: (0.5, 1)

<PXPLogo>:
  text: 'Project X Paris'
  font_size: 30

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
  Image:
    size_hint: (1, 0.1)
    source: 'empty.png'
  HomeBannerWidget:
  ScrollView:
    size_hint: (1, 0.8)
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
  Image:
    size_hint: (1, 0.1)
    source: 'empty.png'
  ImageBannerWidget:
  ScrollView:
    size_hint: (1, 0.8)
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

Builder.load_string(design)

class AuthenticationWidget(BoxLayout):
  def __init__(self, **kwargs):
    super(AuthenticationWidget, self).__init__(**kwargs)
  
  def validate(self):
    if hashlib.sha256(self.ids['attempt'].text).hexdigest() == self.parent.salt:
      self.parent.passwd = self.ids['attempt'].text
      self.clear_widgets()
      self.parent.__init__()
    else:
      self.ids['failure'].text = 'Mot de passe erroné, essayez à nouveau'
      self.ids['attempt'].text = ''

class PXPLogo(Label):
  pass

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

class StoreWidget(BodyLayout):
  def __init__(self, **kwargs):
    super(StoreWidget, self).__init__(**kwargs)
    # for the ScrollView
    self.bind(minimum_height=self.setter('height'))
    # loading images
    #self.load_images()
  
  def load_images(self):
    images = []
    client = paramiko.client.SSHClient()
    client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
    client.connect(
        '178.170.72.68',
        port = 44700,
        username = 'pierre',
        password = self.parent.parent.parent.parent.passwd)
    directory = 'Home/'
    cmd = 'ls /var/www/PXPAppProducts/' + directory
    stdin, stdout, stderr = client.exec_command(cmd)
    for entry in stdout.readlines():
      entry = str(entry).split('\n')[0]
      info = entry.split('.')
      if len(info) == 2 and info[1] == 'jpg':
        entry = entry.split('_')[0]
        if not(entry in images):
          images.append(entry)
    client.close()
    for image in images:
      image += '_0.jpg'
      src = 'http://www.projectxparis.com/PXPAppProducts/'+ directory + image
      self.add_widget(AsyncImageButton(
        source = src,
        allow_stretch = True,
        size_hint = (1, None),
        height = 200
      ))

class RootWidget(BoxLayout):
  salt = '97fde7b312f0d79dbadaeb0c63fd270c9a168ea4a21f060d8cb9bf9000df905d'
  passwd = None
  def __init__(self, **kwargs):
    super(RootWidget, self).__init__(**kwargs)
    # authenticate the wholesaler to the app
    self.clear_widgets()
    self.authenticate()
  
  def authenticate(self):
    if self.passwd != None:
      HW = HomeWidget()
      self.add_widget(HW)
      HW.ids['store'].load_images()
    else:
      self.clear_widgets()
      self.add_widget(AuthenticationWidget())
  
  # remove the store view and show the image
  def show_image(self, source_add):
    self.clear_widgets()
    pw = ProductWidget()
    self.add_widget(pw)
  
  def return_to_root(self):
    self.__init__()
  
  def show_menu(self):
    self.clear_widgets()
    self.add_widget(MenuWidget())
  
  def show_category(self, category):
    self.clear_widgets()
    CW = CategoryWidget()
    self.add_widget(CW)
    CW.update(category)
  
  def show_product(self, source_add):
    self.clear_widgets()
    PW = ProductWidget()
    self.add_widget(PW)
    PW.update(source_add)

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
    self.parent.__init__()
  
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
  
  def update(self, directory):
    directory += '/'
    images = []
    client = paramiko.client.SSHClient()
    client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
    client.connect(
        '178.170.72.68',
        port = 44700,
        username = 'pierre',
        password = self.parent.passwd)
    cmd = 'ls /var/www/PXPAppProducts/' + directory
    stdin, stdout, stderr = client.exec_command(cmd)
    for entry in stdout.readlines():
      entry = str(entry).split('\n')[0]
      info = entry.split('.')
      if len(info) == 2 and info[1] == 'jpg':
        entry = entry.split('_')[0]
        if not(entry in images):
          images.append(entry)
    client.close()
    for image in images:
      image += '_0.jpg'
      src = 'http://www.projectxparis.com/PXPAppProducts/'+ directory + image
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
    client = paramiko.client.SSHClient()
    client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
    client.connect(
        '178.170.72.68',
        port = 44700,
        username = 'pierre',
        password = self.parent.passwd)
    ref = 'cat /home/pierre/PXPAppProducts/' + directory + '/' + \
      name + '_ref.txt'
    price = string.replace(ref, '_ref.txt', '_price.txt')
    stdin, stdout, stderr = client.exec_command(ref)
    for ref in stdout.readlines():
      self.ids['product_reference'].text = 'référence : ' + \
        str(ref).split('\n')[0]
    stdin, stdout, stderr = client.exec_command(price)
    for price in stdout.readlines():
      self.ids['product_price'].text = str(price).split('\n')[0] + '€'
    client.close()
  
  def switch_image(self, source_add):
    self.ids['product_image'].source = source_add
  
  def return_to_root(self):
    self.clear_widgets()
    self.parent.__init__()

class PXPApp(App):
  def build(self):
    # launches the notification service
    if platform == 'android':
      from android import AndroidService
      service = AndroidService(
        'PXPApp',
        'starting notification service... '
      )
      service.start('any argument')
      self.service = service
    return RootWidget()
  
  # so that memory is kept when app is left but not killed
  #   -> does not help
  # FIXME: app freezes when set to background
  def on_pause():
    return True

if __name__ == '__main__':
  PXPApp().run()





