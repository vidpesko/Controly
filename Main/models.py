# Create your models here.
import random
import uuid
import os

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Color(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True)
    hex_value = models.CharField(max_length=8)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hex_value = self.hex_value.replace('#', '')
        self.hex_value = self.hex_value.upper()

    def __str__(self):
        return self.hex_value

class Animation(models.Model):
    user_friendly_name = models.CharField(max_length=100)

    code_name = models.CharField(max_length=30)

    def __str__(self):
        return 'Animacija: ' + self.user_friendly_name

class Module(models.Model):
    user_friendly_name = models.CharField(max_length=100)
    title = models.CharField(max_length=100, blank=True, default='')

    code_name = models.CharField(max_length=100)
    post_value = models.CharField(max_length=100, default='')

    path = models.CharField(max_length=100, default='')

    def __str__(self) -> str:
        return self.user_friendly_name

class Device(models.Model):
    updated = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Device Name
    name = models.CharField(max_length=30, unique=False)
    serial_port_name = models.CharField(max_length=30, default=None, null=True, blank=True)
    root_id = models.CharField(max_length=30, default='controly')
    is_scene = models.BooleanField(default=False)
    scene_name = models.CharField(max_length=30, blank=True)

    # Device Properties - all are set to none, they can be changed when needed:
    state = models.BooleanField(null=True, default=None)

    # Color properties:
    color = models.ForeignKey(Color, on_delete=models.SET_DEFAULT, null=True, default=None, blank=True)
    rest_color = models.ForeignKey(Color, on_delete=models.SET_DEFAULT, null=True, default=None, related_name='REST', blank=True)
    recently_used_colors = models.ManyToManyField(Color, related_name='recently', blank=True)
    recently_used_colors_rest = models.ManyToManyField(Color, related_name='recently_rest', blank=True)

    # Presets / animations
    animation = models.ForeignKey(Animation, on_delete=models.SET_NULL, null=True, default=None, blank=True)

    # Register all the required modules:
    modules = models.ManyToManyField(Module)

    # Changes from Arduino
    last_status = models.BooleanField(default=False)
    changes = models.TextField(blank=True)
    change_time = models.TimeField(blank=True, null=True)

    device_icon_address = models.CharField(max_length=40, blank=True, default='')

    other_info = models.TextField(blank=True)
    def get_url_formatted(self):
        out = self.name
        out = out.replace(' ', '%20')
        out = out.replace("'", '%27')
        return out

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.device_icon_address == '':
            cwd = os.getcwd()
            icons = [i for i in os.listdir(cwd + '/static/assets/img/device_icons/') if i.split('.')[-1] == 'png']
            rand_icon = random.choice(icons)
            # {% static 'assets/img/device_icons/icon1.png' %}
            path = '/assets/img/device_icons/' + rand_icon
            self.device_icon_address = path

            self.save()

    def __str__(self):
        if self.is_scene:
            return self.scene_name + ' is scene: ' + str(self.is_scene) + ' for device: ' + self.name
        else:
            return self.name

class Scenes(models.Model):
    # Scene Name
    name = models.CharField(max_length=30)

    device = models.ForeignKey(Device, on_delete=models.CASCADE)

    # Device Properties - all are set to none, they can be changed when needed:
    state = models.BooleanField(null=True, default=None)

    # Color properties:
    color = models.ForeignKey(Color, on_delete=models.SET_DEFAULT, null=True, default=None, blank=True)
    rest_color = models.ForeignKey(Color, on_delete=models.SET_DEFAULT, null=True, default=None, related_name='rest_color', blank=True)
    recently_used_colors = models.ManyToManyField(Color, related_name='recently_scene', blank=True)
    recently_used_colors_rest = models.ManyToManyField(Color, related_name='recently_rest_scene', blank=True)

    # Presets / animations
    animation = models.ForeignKey(Animation, on_delete=models.SET_NULL, null=True, default=None, blank=True)

    def __str__(self):
        return self.name