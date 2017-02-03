import responses
import tempfile
import os.path
import re
from pprint import pprint
from .komiksowiec import Komiksowiec


@responses.activate
def test_all():
    def file_callback(request):
        if request.url == "http://dilbert.com/?starting_point=03":
            filename = "dilbert_test3.html"
        elif request.url == "http://dilbert.com/?starting_point=06":
            filename = "dilbert_test6.html"
        elif request.url == "http://dilbert.com/?starting_point=00" or request.url == "http://dilbert.com/":
            filename = "dilbert_test0.html"
        elif request.url == "http://garfield.com/":
            filename = "garfield_agegate.html"
        elif request.url == "http://garfield.com/agegate":
            filename = "garfield_agegate.html"
        elif request.url == "http://garfield.com/comic/2017/02/02":
            filename = "garfield_test_yesterday.html"
        elif request.url == "http://garfield.com/comic/2017/02/01":
            filename = "garfield_test_before_yesterday.html"
        elif request.url == "http://garfield.com/comic/":
            filename = "garfield_test_today.html"
        elif request.url == "http://phdcomics.com/comics/archive.php?comicid=1919":
            filename = "phdcomics_test_yesterday.html"
        elif request.url == "http://phdcomics.com/comics/archive.php?comicid=1918":
            filename = "phdcomics_test_before_yesterday.html"
        elif request.url == "http://phdcomics.com/":
            filename = "phdcomics_test_today.html"
        else:
            print(request.url)
            return 404, [], ''

        basepath = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(basepath, 'comics', filename)) as f:
            return 200, [], f.read()

    responses.add_callback(responses.GET,
                           re.compile('http://.*'),
                           callback=file_callback)
    responses.add_callback(responses.POST,
                           re.compile('http://.*'),
                           callback=file_callback)

    def log(text):
        print(text)

    with tempfile.TemporaryDirectory() as tmpdir:
        k = Komiksowiec(log_callback=log, cache_dir=tmpdir, test=True)

        assert k.update() == 9

        comics = k.get_comics()
        assert len(comics) == 9

        for episode in comics:
            # assert k.image_cache.is_cached(episode.image_url) is True
            # This could work if I had images mocked
            pass
