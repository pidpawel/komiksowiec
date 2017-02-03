import os.path
import hashlib
import requests


class ImageCache:
    '''Stores the image copies on disk or retrieves it from the internet and caches'''

    def __init__(self, cache_dir=None):
        '''
        :param cache_dir: directory to store cache into, otherwise ~/.cache/komiksowiec
        '''
        if cache_dir:
            self.directory = cache_dir
        else:
            self.directory = os.path.join(os.path.expanduser('~'), '.cache', 'komiksowiec')

    def _hash_url(self, url):
        '''Helper function for generating cache filenames.

        :param url: url of the image to hash
        :return: certain hash of the url
        '''
        return hashlib.sha256(url.encode()).hexdigest()

    def _get_image_path(self, url):
        '''Returns the image path (does *not* try to cache it if not).

        :param url: url of the image to retrieve path of
        :return: filesystem path to the image on disk
        '''
        return os.path.join(self.directory, self._hash_url(url))

    def _download(self, url):
        '''Makes actual download. (Always download.)

        :param url: url of the image to download
        '''
        filename = self._get_image_path(url)

        try:
            r = requests.get(url)
        except requests.exceptions.RequestException:
            pass
        else:
            if r.status_code == 200:
                with open(filename, 'wb') as f:
                    f.write(r.content)

    def is_cached(self, url):
        '''Checks if given image is in cache.

        :param url: url of the image to check
        :return: True if file is on a disk
        '''
        return os.path.isfile(self._get_image_path(url))

    def cache_image(self, url, force=False):
        '''Retrieves the image and stores it in the local cache.

        :param url: url of the image to cache
        :param force: if True then always redownloads
        '''
        if not self.is_cached(url) or force is True:
            self._download(url)

    def get_image_path(self, url):
        '''Gets the path of cached image (or tries to download it when not in cache).

        :param url: url of the image to obtain
        :return: path of the file on a disk
        '''
        path = self._get_image_path(url)

        if not self.is_cached(path):
            self.cache_image(url)

        return path

    def get_image(self, url):
        '''Gets the image contents from cache (preferred) or tries to download it and cache.

        :param url: url of the image
        :return: image contents
        '''
        filename = self.get_image_path(url)

        return open(filename).read()
