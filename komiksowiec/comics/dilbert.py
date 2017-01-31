import requests
from lxml import html
from ..crawler import *
from ..episode import Episode


class Dilbert(Crawler):
    def __init__(self, image_cache=None):
        self.image_cache = image_cache

    def crawl(self, depth=1):
        episodes = []
        for i in range(depth):
            url = "http://dilbert.com/?starting_point={:02d}".format(i * 3)

            r = requests.get(url)
            if r.status_code == 200:
                tree = html.fromstring(r.content)
                images = tree.xpath('//img[contains(@class, "img-comic")]')

                for image in images:
                    title = image.get('alt')
                    series = 'Dilbert'
                    if '-' in title:
                        try:
                            split = title.split('-')
                            title = split[0].strip() or 'None'
                            series = split[1].strip() or series
                        except:
                            pass

                    episode = Episode(
                        name=title,
                        series=series,
                        image_url=image.get('src'))

                    if self.image_cache:
                        self.image_cache.cache_image(image_url)

                    episodes.append(episode)

        return episodes
