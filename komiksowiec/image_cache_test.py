import tempfile
import responses
import os.path
from .image_cache import ImageCache


@responses.activate
def test_cache():
    basepath = os.path.dirname(os.path.abspath(__file__))
    file_contents = open(os.path.join(basepath, 'image_cache_image0.svg')).read()
    image_url = 'http://static.hskrk.pl/logo.svg'

    responses.add(responses.GET, 'http://static.hskrk.pl/logo.svg',
                  content_type='image/svg+xml', status=200,
                  body=file_contents)

    with tempfile.TemporaryDirectory() as tmpdir:
        c = ImageCache(cache_dir=tmpdir)
        c.cache_image(image_url)
        assert c.get_image(image_url) == file_contents
        del c

        d = ImageCache(cache_dir=tmpdir)
        assert d.get_image(image_url) == file_contents
