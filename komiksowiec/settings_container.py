import os.path
import json


class SettingsContainer:
    '''Container for storing settings. With basic defaulting support.'''
    def __init__(self, cache_dir=None):
        '''
        :param cache_dir: directory to store settings into, otherwise ~/.cache/komiksowiec
        '''
        if cache_dir:
            self.directory = cache_dir
        else:
            self.directory = os.path.join(os.path.expanduser('~'), '.cache', 'komiksowiec')

        self.filename = os.path.join(self.directory, 'settings.json')
        self.defaults = {}
        self.settings = {}

        self.read()

    def read(self):
        '''Method rereading settings file.'''
        if not os.path.isfile(self.filename):
            return

        with open(self.filename, 'r') as f:
            self.settings = json.loads(f.read())

    def save(self):
        '''Method flushing current settings to disk.'''
        with open(self.filename, 'w') as f:
            f.write(json.dumps(self.settings))

    def register_default(self, name, value):
        '''Method to register default value for a given key. Must be called before any .get call using this key.

        :param name: name of the key to store default for
        :param value: default value
        '''
        self.defaults[name] = value

    def get(self, name):
        '''Method for getting the setting value.

        :param name: key for which try to obtain a value
        :returns: value under requested key
        '''
        if name in self.settings:
            return self.settings[name]
        elif name in self.defaults:
            v = self.defaults[name]
            self.settings[name] = v
            return v
        else:
            raise NotImplementedError

    def set(self, name, value):
        '''Sets a given key with a givel value.

        :param name: key name
        :param value: key value
        '''
        self.settings[name] = value
