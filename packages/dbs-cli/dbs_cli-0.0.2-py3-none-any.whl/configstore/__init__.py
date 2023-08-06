import os

from .utils import (get_config_dir, create_config, load_configs,
                   get_config_size, get_configs, set_configs,
                   has_configs, delete_configs, clear_configs)


class ConfigStore:

    def __init__(self, name, defaults={}, global_config_path=False):
        self.name = name
        self.defaults = defaults
        self.global_config_path = global_config_path

        self.config_dir = get_config_dir()

        if self.global_config_path:
            self.path_prefix = os.path.join(name, 'config.json')
            path_entry = name
        else:
            self.path_prefix = os.path.join('configstore',
                                            '{}.json'.format(name))
            path_entry = 'configstore'

        self.path = os.path.join(self.config_dir, self.path_prefix)
        create_config(self.path, self.defaults, path_entry=path_entry)
        self.obj = load_configs(self.path)
        self.size = get_config_size(self.path)

    def all(self, obj=None):
        if obj:
            self.set(obj)

        json_configs = load_configs(self.path)
        return json_configs

    def get(self, key):
        value = get_configs(self.path, key)
        return value

    def set(self, key, value=None):
        if isinstance(key, dict):
            set_object = key
            set_configs(self.path, obj=set_object)
        else:
            if not value:
                raise KeyError("KeyError: param value not provided")
            set_configs(self.path, key=key, value=value)

    def has(self, key):
        return has_configs(self.path, key)

    def delete(self, key):
        delete_configs(self.path, key)

    def clear(self):
        clear_configs(self.path)

