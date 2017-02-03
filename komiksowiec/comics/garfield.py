import requests
from lxml import html
from ..crawler import *
from ..episode import Episode


# http://docs.python-guide.org/en/latest/scenarios/scrape/
class Garfield(Crawler):
    def __init__(self, http=False):
        self.http = http
        self.session = requests.Session()

    def _verify_age(self):
        url = "https://garfield.com/"

        if self.http:
            url = url.replace('https', 'http')

        r = self.session.get(url)
        tree = html.fromstring(r.content)
        token = tree.xpath('//input[@name = "_token"]')

        if len(token) == 0:
            return False

        token = token[0].get('value')

        url = "https://garfield.com/agegate"

        if self.http:
            url = url.replace('https', 'http')

        self.session.post(url, data={
            '_token': token,
            'year': 1970,
            'month': 1,
            'day': 1
        })

        return True

    def crawl(self, depth=3):
        # This might be called from a constructor but it might throw a network error so it stays here
        if not self._verify_age():
            return []

        episodes = []

        url = "https://garfield.com/comic/"

        for i in range(depth):
            if self.http:
                url = url.replace('https', 'http')

            r = self.session.get(url)

            if r.status_code == 200:
                tree = html.fromstring(r.content)

                image = tree.xpath('//img[@width = 1200]')
                if len(image) == 0:
                    break
                image = image[0].get('src')

                urls = tree.xpath('//a[contains(@class, "btn btn-default btn-xs")]')
                if len(urls) == 0:
                    break

                url = urls[0].get('href')

                title = tree.xpath('//title/text()')
                if len(title) == 0:
                    break

                title = title[0]

                if '|' not in title:
                    break

                series, title = title.split('|')
                series = series.strip()
                title = title.strip()

                episode = Episode(
                    name=title,
                    series=series,
                    image_url=image)

                episodes.append(episode)

        return episodes
