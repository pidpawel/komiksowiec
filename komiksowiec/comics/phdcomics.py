import requests
from lxml import html
from ..crawler import *
from ..episode import Episode


# http://docs.python-guide.org/en/latest/scenarios/scrape/
class PHDComics(Crawler):
    def crawl(self, depth=3):
        episodes = []

        url = "http://phdcomics.com/"

        for i in range(depth):
            r = requests.get(url)

            if r.status_code == 200:
                text = r.content.decode().replace('--!>', '-->')
                tree = html.fromstring(text)

                image = tree.xpath('//img[@id = "comic2"]')
                if len(image) == 0:
                    break
                image = image[0].get('src')

                urls = tree.xpath('//a[img[@width=49]]')
                if len(urls) == 0:
                    break
                url = urls[0].get('href')

                title = tree.xpath('//title/text()')
                if len(title) == 0:
                    break

                title = title[0]

                if ':' not in title:
                    break

                series, title = title.split(':')
                series = series.strip()
                title = title.strip()

                episode = Episode(
                    name=title,
                    series=series,
                    image_url=image)

                episodes.append(episode)

        return episodes
