import os.path
from .episode import Episode
from .crawler import get_crawlers
from .image_cache import ImageCache
from .episode_storage import EpisodeStorage


class Komiksowiec:
    def __init__(self, cache_dir=None):
        if cache_dir:
            self.cache_dir = cache_dir
        else:
            self.cache_dir = os.path.join(os.path.expanduser('~'), '.cache', 'komiksowiec')

        # @TODO create cache dir

        self.episode_storage = EpisodeStorage(cache_dir=self.cache_dir)
        self.image_cache = ImageCache(cache_dir=self.cache_dir)

        self.crawlers = [crawler_class() for crawler_class in get_crawlers()]

    def update(self):
        ''' Do a periodic update (crawl, delete old ones,…) '''
        new_episodes = []

        # Get episodes
        for crawler in self.crawlers:
            new_episodes += crawler.crawl()

        # Cache images
        for episode in new_episodes:
            self.image_cache.cache_image(episode.image_url)

        # Save only new episodes (EpisodeStorage guarantees it)
        for episode in new_episodes:
            self.episode_storage.add_episode(episode)

        self.episode_storage.save()

    def get_comics(self):
        ''' Retrieves a current comic list (archieved or new ones) '''
        return self.episode_storage.list_episodes()
