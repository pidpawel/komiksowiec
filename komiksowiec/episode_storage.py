import os.path
import csv
from .episode import Episode


class EpisodeStorage:
    '''Stores episode data in CSV file.'''
    def __init__(self, cache_dir=None):
        '''
        :param cache_dir: directory to store cache into, otherwise ~/.cache/komiksowiec
        '''
        if cache_dir:
            self.directory = cache_dir
        else:
            self.directory = os.path.join(os.path.expanduser('~'), '.cache', 'komiksowiec')

        self.filename = os.path.join(self.directory, 'episodes.csv')

        self.episodes = []
        self._load_db()

    def _load_db(self):
        self.episodes.clear()

        if not os.path.isfile(self.filename):
            return

        with open(self.filename) as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                episode = Episode(**row)
                self.episodes.append(episode)

    def _flush_db(self):
        with open(self.filename, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=Episode.fields)

            writer.writeheader()
            for episode in self.episodes:
                writer.writerow(episode.as_dict())

    def has_episode(self, new_episode):
        '''Finds episode by attributes.

        :param new_episode: Episode object to compare with
        :type new_episode: Episode
        :return: returns whether similar episode is in the database
        :rtype: bool
        '''
        compare = ['name', 'series', 'image_url']

        for episode in self.episodes:
            found = 0

            for key in compare:
                if getattr(episode, key) == getattr(new_episode, key):
                    found += 1

            if found == len(compare):
                return True

        return False

    def add_episode(self, episode):
        '''Adds the episode to memory.

        :param episode: Episode object to add
        :type episode: Episode
        '''
        if not self.has_episode(episode):
            self.episodes.append(episode)

    def list_episodes(self):
        '''Returns the episodes stored in memory sorted by date.

        :return: list of episodes
        :rtype: [Episode object, Episode object,...]
        '''
        return sorted(self.episodes, key=lambda episode: episode.date, reverse=True)

    def save(self):
        '''Flushes the elements sotred in the memory to disk.'''
        self._flush_db()
