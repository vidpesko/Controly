
# ! For each module, there must be a function, that will be called when saving POST request from website and will do all the data processing
# ? Function will be given two parameters - input data, device ==> AND SHOULD RETURN PROCESS DATA IN SHAPE, THAT IS READABLE TO THE ACTUAL DEVICE
# ~ Function name should be same as code_name of module

from .models import Color, Animation

def active_color_picker(input: str, device):
    input = input.split('#')[-1]

    color, created = Color.objects.get_or_create(hex_value=input.upper())

    device.color = color
    device.recently_used_colors.add(color)

    return color.hex_value

def rest_color_picker(input: str, device):
    input = input.split('#')[-1]

    color, created = Color.objects.get_or_create(hex_value=input.upper())

    device.rest_color = color
    device.recently_used_colors_rest.add(color)

    return color.hex_value

def state_switch(input: str, device):
    state = True if input == 'true' else False
    device.state = state

    return state

def animation_picker(input: str, device):
    # ? Animation function is given code_name of selected animation
    animation = Animation.objects.get(code_name=input)
    device.animation = animation

    return input

def scene_picker(input: str, device):
    return input

def scheduler(input: str, device):
    print(input)
    return input

def turn_on_range(input: str, device):
    print(input)
    return input

MODULES_FUNCTIONS = {
    'active_color_picker': active_color_picker,
    'rest_color_picker': rest_color_picker,
    'state_switch': state_switch,
    'animation_picker': animation_picker,
    'scene_picker': scene_picker,
    'scheduler': scheduler,
    'turn_on_range': turn_on_range,
}

def save_device_data(post, device, used_modules, new_data=None):
    for module in used_modules:
        post_value = post[module.post_value]
        mod_func = MODULES_FUNCTIONS[module.code_name]

        if new_data is not None:
            new_data[module.post_value] = mod_func(post_value, device)
        else:
            mod_func(post_value, device)