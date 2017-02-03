import responses
import os.path
import re
from pprint import pprint
from . import garfield


@responses.activate
def test_crawler():
    def file_callback(request):
        if request.url == "http://garfield.com/agegate":
            filename = "garfield_agegate.html"
        elif request.url == "http://garfield.com/comic/2017/02/02":
            filename = "garfield_test_yesterday.html"
        elif request.url == "http://garfield.com/comic/2017/02/01":
            filename = "garfield_test_before_yesterday.html"
        elif request.url == "http://garfield.com/comic/":
            filename = "garfield_test_today.html"
        else:
            print(request.url)
            return 404, [], ''

        basepath = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(basepath, filename)) as f:
            return 200, [], f.read()

    responses.add_callback(responses.GET,
                           re.compile('http://garfield\.com/.*'),
                           callback=file_callback)
    responses.add_callback(responses.POST,
                           re.compile('http://garfield\.com/.*'),
                           callback=file_callback)

    g = garfield.Garfield(http=True)
    results = g.crawl(depth=3)

    assert len(results) == 3

    # for i, episode in enumerate(results):
    #     print('''assert results[{i}].name == '{episode.name}' '''.format(episode=episode, i=i))
    #     print('''assert results[{i}].series == '{episode.series}' '''.format(episode=episode, i=i))
    #     print('''assert results[{i}].image_url == '{episode.image_url}' '''.format(episode=episode, i=i))
    #     print()

    assert results[0].name == 'Daily Comic Strip on February 3rd, 2017'
    assert results[0].series == 'Garfield'
    assert results[0].image_url == 'https://d1ejxu6vysztl5.cloudfront.net/comics/garfield/2017/2017-02-03.gif'

    assert results[1].name == 'Daily Comic Strip on February 2nd, 2017'
    assert results[1].series == 'Garfield'
    assert results[1].image_url == 'https://d1ejxu6vysztl5.cloudfront.net/comics/garfield/2017/2017-02-02.gif'

    assert results[2].name == 'Daily Comic Strip on February 1st, 2017'
    assert results[2].series == 'Garfield'
    assert results[2].image_url == 'https://d1ejxu6vysztl5.cloudfront.net/comics/garfield/2017/2017-02-01.gif'
