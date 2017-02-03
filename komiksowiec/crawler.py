from glob import glob
import importlib
import os.path
import inspect


class Crawler:
    '''
    Crawler interface
    All Comic crawlers should implement this
    '''
    def crawl(self):
        '''
        Returns a list of crawled Episodes
        '''
        raise NotImplemented


def get_crawlers():
    crawlers = []

    base_path = os.path.dirname(os.path.abspath(__file__))
    candidates = glob(base_path + '/comics/*.py')

    for candidate in candidates:
        if '_test' in candidate or '__init__' in candidate:
            continue

        candidate = os.path.splitext(os.path.basename(candidate))[0]

        module = importlib.import_module('.comics.' + candidate, 'komiksowiec')

        for element in dir(module):
            element = getattr(module, element)

            if inspect.isclass(element) and issubclass(element, Crawler) and not element == Crawler:
                crawlers.append(element)

    return crawlers
