import os
import shutil
from distutils.dir_util import copy_tree
import uuid


def duplicate_folder(source_folder, destination_folder):
    # if '.DS_Store' in os.listdir(source_folder):
        # os.remove(source_folder + '/.DS_Store')
    copy_tree(source_folder, destination_folder)

def create_universal_code():
    id = str(uuid.uuid4())
    return create_controly_code(id, id, id), id

def create_controly_code(name, serial, modules):
    cwd = os.getcwd()
    src = cwd + '/Communication/ControlyDevice-'
    
    dst = cwd + '/static/CreatedCode/ControlyDevice-' + name
    if os.path.exists(dst):
        shutil.rmtree(dst)

    duplicate_folder(src, dst)
    # ? Duplicating venv folder
    duplicate_folder(cwd + '/venv', dst + '/venv')

    device_specific_path = dst + '/device_specific.py'
    r = open(device_specific_path, 'r')
    content = [line for line in r]
    r.close()

    f = open(device_specific_path, 'w')

    lines = []
    i = 0

    for line in content:
        # print(i, line.replace('\n', ''), 'h')
        line = line.replace('\n', '')
        if line == "DEVICE_NAME=''":
            line = f'DEVICE_NAME="{name}"'
        elif line == "DEVICE_SERIAL_PORT=''":
            line = f"DEVICE_SERIAL_PORT='{serial}'"

        lines.append(line + '\n')
        i += 1

    # print(lines)
    f.writelines(lines)
    f.close()

    return dst


def compress_code(source, destination):
    shutil.make_archive(destination, 'zip', source)

def compare_bool_str(str_val):
    if str_val == 'True':
        return True
    elif str_val == 'False':
        return False
    else:
        return None