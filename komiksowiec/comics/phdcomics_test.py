import responses
import os.path
import re
from pprint import pprint
from . import phdcomics


@responses.activate
def test_crawler():
    def file_callback(request):
        if request.url == "http://phdcomics.com/comics/archive.php?comicid=1919":
            filename = "phdcomics_test_yesterday.html"
        elif request.url == "http://phdcomics.com/comics/archive.php?comicid=1918":
            filename = "phdcomics_test_before_yesterday.html"
        elif request.url == "http://phdcomics.com/":
            filename = "phdcomics_test_today.html"
        else:
            print(request.url)
            return 404, [], ''

        basepath = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(basepath, filename)) as f:
            return 200, [], f.read()

    responses.add_callback(responses.GET,
                           re.compile('http://phdcomics\.com/.*'),
                           callback=file_callback)

    p = phdcomics.PHDComics()
    results = p.crawl(depth=3)

    assert len(results) == 3

    # for i, episode in enumerate(results):
    #     print('''assert results[{i}].name == '{episode.name}' '''.format(episode=episode, i=i))
    #     print('''assert results[{i}].series == '{episode.series}' '''.format(episode=episode, i=i))
    #     print('''assert results[{i}].image_url == '{episode.image_url}' '''.format(episode=episode, i=i))
    #     print()

    assert results[0].name == 'The new busy'
    assert results[0].series == 'PHD Comics'
    assert results[0].image_url == 'http://www.phdcomics.com/comics/archive/phd020117s.gif'

    assert results[1].name == 'How I Write'
    assert results[1].series == 'PHD Comics'
    assert results[1].image_url == 'http://www.phdcomics.com/comics/archive/phd012717s.gif'

    assert results[2].name == 'Rihanna'
    assert results[2].series == 'PHD Comics'
    assert results[2].image_url == 'http://www.phdcomics.com/comics/archive/phd012517s.gif'
