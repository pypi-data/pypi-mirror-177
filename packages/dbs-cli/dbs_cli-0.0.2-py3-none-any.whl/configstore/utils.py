import os
import sys
import json


def get_config_dir():
    if sys.platform == "win32":
        app_config_dir = os.getenv("LOCALAPPDATA")
    else:
        app_config_dir = os.getenv("HOME")
        if os.getenv("XDG_CONFIG_HOME"):
            app_config_dir = os.getenv("XDG_CONFIG_HOME")

    config_dir = os.path.join(app_config_dir, ".localconfig")
    return config_dir


def create_path(path):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
        return True


def create_config(path, defaults, **kwargs):
    config_dir = get_config_dir()
    path_entry = os.path.join(config_dir, kwargs["path_entry"])
    create_path(path_entry)
    if os.path.exists(path_entry) and not os.path.isfile(path):
        with open(path, 'w') as cf:
            json.dump(defaults, cf)


def create_config_path_sync(path):
    path_entry = os.path.dirname(path)
    create_config(path, {}, path_entry=path_entry)


def load_configs(path):
    create_config_path_sync(path)
    if os.path.isfile(path):
        with open(path, 'r') as fp:
            json_configs = dict(json.load(fp))
        return json_configs


def write_configs(path, json_data):
    with open(path, 'w') as fp:
        json.dump(json_data, fp)


def set_configs(path, key=None, value=None, obj=None):
    json_configs = load_configs(path)

    if obj is None:
        json_configs.update(dot_notation(key, value))
    else:
        for jkey, jval in obj.items():
            json_configs.update(dot_notation(jkey, jval))

    write_configs(path, json_configs)


def get_configs(path, key):
    json_configs = load_configs(path)
    value = json_configs[key]
    return value


def has_configs(path, key):
    json_configs = load_configs(path)

    if key in json_configs:
        return True

    return False


def delete_configs(path, key):
    json_configs = load_configs(path)
    json_configs.pop(key)
    write_configs(path, json_configs)


def clear_configs(path):
    write_configs(path, {})


def get_config_size(path):
    json_configs = load_configs(path)
    return len(json_configs)


def dot_notation(key, value):
    key = key.replace("\\.", "~=~")
    key_arr = key.split('.')[::-1]

    for arr in key_arr:
        value = {arr.replace('~=~', '.'): value}

    return value
