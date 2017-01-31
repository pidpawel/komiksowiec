import responses
import os.path
import re
from pprint import pprint
from . import dilbert


@responses.activate
def test_crawler():
    def file_callback(request):
        if request.url == "http://dilbert.com/?starting_point=03":
            filename = "dilbert_test3.html"
        elif request.url == "http://dilbert.com/?starting_point=06":
            filename = "dilbert_test6.html"
        elif request.url == "http://dilbert.com/?starting_point=00" or request.url == "http://dilbert.com/":
            filename = "dilbert_test0.html"
        else:
            print(request.url)
            return 404, [], ''

        basepath = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(basepath, filename)) as f:
            return 200, [], f.read()

    responses.add_callback(responses.GET, re.compile('http://dilbert\.com/(\?starting_point=\d+)?'),
                           callback=file_callback)

    d = dilbert.Dilbert()
    results = d.crawl()

    assert len(results) == 9

    # for i, episode in enumerate(results):
    #     print('''assert results[{i}].name == '{episode.name}' '''.format(episode=episode, i=i))
    #     print('''assert results[{i}].series == '{episode.series}' '''.format(episode=episode, i=i))
    #     print('''assert results[{i}].image_url == '{episode.image_url}' '''.format(episode=episode, i=i))
    #     print()

    assert results[0].name == 'Remember Or Rumor'
    assert results[0].series == 'Dilbert by Scott Adams'
    assert results[0].image_url == 'http://assets.amuniversal.com/c0187630b3f8013428f5005056a9545d'

    assert results[1].name == 'Wally\'s Red File Gets Him Out Of Work'
    assert results[1].series == 'Dilbert by Scott Adams'
    assert results[1].image_url == 'http://assets.amuniversal.com/be300c60b3f8013428f5005056a9545d'

    assert results[2].name == 'The Illusion Of Work'
    assert results[2].series == 'Dilbert by Scott Adams'
    assert results[2].image_url == 'http://assets.amuniversal.com/bc7ebe70b3f8013428f5005056a9545d'

    assert results[3].name == 'Elbonians Jumping Off Roof'
    assert results[3].series == 'Dilbert by Scott Adams'
    assert results[3].image_url == 'http://assets.amuniversal.com/baaf4240b3f8013428f5005056a9545d'

    assert results[4].name == 'Rather Eat Garbage'
    assert results[4].series == 'Dilbert by Scott Adams'
    assert results[4].image_url == 'http://assets.amuniversal.com/b8fe3d00b3f8013428f5005056a9545d'

    assert results[5].name == 'None'
    assert results[5].series == 'Dilbert by Scott Adams'
    assert results[5].image_url == 'http://assets.amuniversal.com/9a71dd00acb001341c1f005056a9545d'

    assert results[6].name == 'Fairness Is For Kids And Idiots'
    assert results[6].series == 'Dilbert by Scott Adams'
    assert results[6].image_url == 'http://assets.amuniversal.com/f4f165d0ae6b01341f1d005056a9545d'

    assert results[7].name == 'New Hire Makes More'
    assert results[7].series == 'Dilbert by Scott Adams'
    assert results[7].image_url == 'http://assets.amuniversal.com/f33d7ed0ae6b01341f1d005056a9545d'

    assert results[8].name == 'Coaching Alice'
    assert results[8].series == 'Dilbert by Scott Adams'
    assert results[8].image_url == 'http://assets.amuniversal.com/f187cbb0ae6b01341f1d005056a9545d'
