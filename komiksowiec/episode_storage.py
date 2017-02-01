import os.path
import csv
from .episode import Episode


class EpisodeStorage:
    '''
    Stores episode data in CSV file
    '''
    def __init__(self, cache_dir=None):
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
                # @TODO date formatting
                self.episodes.append(episode)

    def _flush_db(self):
        with open(self.filename, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=Episode.fields)

            writer.writeheader()
            for episode in self.episodes:
                writer.writerow(episode.as_dict())
                # @TODO date formatting

    def has_episode(self, new_episode):
        ''' Finds episode by attributes '''
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
        if not self.has_episode(episode):
            self.episodes.append(episode)

    def list_episodes(self):
        return self.episodes

    def save(self):
        self._flush_db()
