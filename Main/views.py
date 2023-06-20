from .models import *
from . import modules
from Communication.mqtt_server import publish, changes_dict
from Communication.utils import create_controly_code, compress_code, create_universal_code, compare_bool_str

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

import shutil


@login_required
def choose_device(request):
    devices = Device.objects.filter(is_scene=False)
    modules = Module.objects.all()

    context = {'devices': devices, 'all_modules': modules}
    return render(request, 'Main/device_selection.html', context)


@login_required
def device_page(request, device_name):
    # ! Get Device
    device = Device.objects.get(name=device_name, is_scene=False)
    root_id = device.root_id
    TOPIC_NAME = 'Controly/vid/' + device.name

    # ! Get modules, that are used by the device
    used_modules = device.modules.all()

    other_info = device.other_info.split(';')
    num_of_leds = None
    leds_range = None
    if Module.objects.get(code_name='turn_on_range') in used_modules:
        for info in other_info:
            info = info.split('=')
            if info[0] == 'NUM_OF_LEDS':
                num_of_leds = int(info[1])
                leds_range = []
                for i in range(0, 10):
                    leds_range.append(i)
                break

    # ! Get all registered modules, animations and users
    all_modules = Module.objects.all()
    all_scenes = Device.objects.filter(is_scene=True, name=device.name)
    animations = Animation.objects.all()
    users = User.objects.all()

    # * If device is using color or rest_color modules, get recently used colors
    recently_used_colors = None
    recently_used_rest_colors = None
    if Module.objects.get(code_name='active_color_picker') in used_modules:
        recently_used_colors = device.recently_used_colors.all()[:5]
    if Module.objects.get(code_name='rest_color_picker') in used_modules:
        recently_used_rest_colors = device.recently_used_colors_rest.all()[:5]

    context = {'device': device, 'recently_used': recently_used_colors, 'recently_used_rest': recently_used_rest_colors, 'real_device': device, 'modules': used_modules, 'leds_range': leds_range, 'all_modules': all_modules, 'animations': animations, 'users': users, 'scenes': all_scenes, 'id': root_id}

    # ? New data dictionary will store all the DEVICE READABLE CODE => this dict will be sent to the arduino/device
    new_data = {}

    # ! Processing POST request
    if request.method == 'POST':
        post = request.POST
        if post['post_form_type'] == 'device':
            name = post['serial_port_name']
            device.serial_port_name = name
            device.save()
            device_changes = [{'field': 'DEVICE_SERIAL_PORT', 'value': name}]
            publish(TOPIC_NAME, device_changes, msg_type='device_change', json_param=True)
        else:
            modules.save_device_data(post, device, used_modules, new_data=new_data)

            # ? Updated by
            device.updated_by = request.user
            device.save()

            # * Send data to device
            publish(TOPIC_NAME, new_data, json_param=True)

            # messages.success(request, 'helo')

            # ? Add to scene -> create new Device Model, which will be unchangeable
            # TODO: user field on scenes
            if post['add_to_scene'] == 'true':
                new_scene_name = post['new_scene_name']
                new_scene = Device.objects.create(name=device.name, scene_name=new_scene_name, root_id='vidi', is_scene=True)
                modules.save_device_data(post, new_scene, used_modules)
                new_scene.save()
                print('My scene dict is this', new_scene.__dict__)

    # ! Code for loading scenes
    elif request.method == 'GET':
        try:
            scene_name = request.GET['scene']
            scene = Device.objects.get(scene_name=scene_name)
            context['real_device'] = device
            context['device'] = scene
        except:
            print('Scene doesnt exist or get request doesnt contain scene name')

    return render(request, 'Main/device_page.html', context)


# ! Login / Logout / Change Password Views
def loginForm(request):
    context = {}

    if request.user.is_authenticated:
        return redirect('choose')

    if request.method == 'POST':
        user_input = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(
                Q(username=user_input) |
                Q(email=user_input)
            )
            print('valid')
        except:
            messages.error(request, 'Neznan uporabnik!')
            return render(request, "Main/pages-login.html", context)

        user = authenticate(request, username=user.username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Uspesna prijava!')
            return redirect('choose')
        else:
            messages.error(request, 'Nepravilno geslo!')
            return render(request, "Main/pages-login.html", context)

    context = {}
    return render(request, 'Main/pages-login.html', context)


def logoutForm(request):
    logout(request)
    return redirect('login')


@login_required
def change_password(request):
    user = request.user

    if request.method == 'POST':
        new_password = request.POST.get('newPassword')
        user.set_password(new_password)
        user.save()
        messages.success(request, 'Uspesna zamenjava!')
        user = authenticate(request, username=user.username, password=new_password)
        login(request, user)
        redirect('choose')

    return render(request, 'Main/change-password.html')


def add_device(request):
    if request.method == 'GET':
        name, serial_port_name, modules, universal, create_new = request.GET.get('name'), request.GET.get('serial'), request.GET.getlist('modules'), request.GET.get('uni'), request.GET.get('create_new')

        universal = compare_bool_str(universal)
        create_new = compare_bool_str(create_new)

        if not universal:
            # try:
                # ? Controly code is created at /static/CreatedCode/ControlyDevice-< device_name >
            filepath = create_controly_code(name, serial_port_name, modules)
            # except:
                # return HttpResponse('Niso bili vneseni vsi podatki za napravo')

            # ? Compressing code -> to new zip file with the file path < device_name >.zip

            if create_new:
                # ? Adding device (if it doesnt exist)
                try:
                    device = Device.objects.get(name=name)
                except:
                    # ~ it doesnt exist
                    device = Device(name=name, serial_port_name=serial_port_name)

                for mod in modules:
                    # Get module object
                    module = Module.objects.get(code_name=mod)
                    device.modules.add(module)
            
                device.save()
        elif universal:
            filepath, name = create_universal_code()

        zip_path = filepath[53:]
        compress_code(filepath, zip_path)
        
        context = {'device':name}
        return render(request, 'Main/download_page.html', context)
    else:
        return HttpResponse('Nekaj je slo narobe! Ups :(')


def delete_code(request):
    path = request.GET.get('path')
    os.remove(os.getcwd() + path)
    shutil.rmtree(os.getcwd() + path[:-4])
    return redirect('choose')