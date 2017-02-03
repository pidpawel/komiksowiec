import os.path
import os
from .episode import Episode
from .crawler import get_crawlers
from .image_cache import ImageCache
from .episode_storage import EpisodeStorage
from .settings_container import SettingsContainer


class Komiksowiec:
    def __init__(self, log_callback=None, cache_dir=None, test=False):
        self.log_callback = log_callback

        if cache_dir:
            self.cache_dir = cache_dir
        else:
            self.cache_dir = os.path.join(os.path.expanduser('~'), '.cache', 'komiksowiec')

        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

        self.episode_storage = EpisodeStorage(cache_dir=self.cache_dir)
        self.image_cache = ImageCache(cache_dir=self.cache_dir)

        self.settings = SettingsContainer(cache_dir=self.cache_dir)
        self.settings.register_default('update_interval', 15)

        self.crawlers = [crawler_class(test=test) for crawler_class in get_crawlers()]

    def _log(self, text):
        if self.log_callback:
            self.log_callback(text)

    def update(self):
        ''' Do a periodic update (crawl, delete old ones,…) '''
        new_episodes = []
        self._log('Crawling...')

        # Get episodes
        for crawler in self.crawlers:
            self._log('Crawling {}...'.format(crawler.__class__.__name__))
            new_episodes += crawler.crawl()

        self._log('Got {} episodes.'.format(len(new_episodes)))

        # Cache images
        for episode in new_episodes:
            self._log('Caching image for {}'.format(episode))
            self.image_cache.cache_image(episode.image_url)

        # Save only new episodes (EpisodeStorage guarantees it)
        self._log('Saving new episodes...')
        for episode in new_episodes:
            self.episode_storage.add_episode(episode)

        self.episode_storage.save()
        self._log('Done!')

        return len(new_episodes)

    def get_comics(self):
        ''' Retrieves a current comic list (archieved or new ones) '''
        return sorted(self.episode_storage.list_episodes(), key=lambda episode: episode.date, reverse=True)
