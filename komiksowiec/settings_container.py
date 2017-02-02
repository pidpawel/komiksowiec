import os.path
import json


class SettingsContainer:
    def __init__(self, cache_dir):
        if cache_dir:
            self.directory = cache_dir
        else:
            self.directory = os.path.join(os.path.expanduser('~'), '.cache', 'komiksowiec')

        self.filename = os.path.join(self.directory, 'settings.json')
        self.defaults = {}
        self.settings = {}

        self.read()

    def read(self):
        if not os.path.isfile(self.filename):
            return

        with open(self.filename, 'r') as f:
            self.settings = json.loads(f.read())

    def save(self):
        with open(self.filename, 'w') as f:
            f.write(json.dumps(self.settings))

    def register_default(self, name, value):
        self.defaults[name] = value

    def get(self, name, default=None):
        if name in self.settings:
            return self.settings[name]
        elif name in self.defaults:
            v = self.defaults[name]
            self.settings[name] = v
            return v
        else:
            raise NotImplementedError

    def set(self, name, value):
        self.settings[name] = value
