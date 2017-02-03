from datetime import datetime


class Episode:
    '''Class for storing episode data.'''
    fields = ['date', 'series', 'name', 'image_url']

    def __init__(self, name, series, image_url, date=None):
        '''

        :param name: name/title of the episode
        :param series: name of the series episode belongs to
        :param image_url: url to the episode image
        :param date: date of publication. If None defaults to current time
        '''
        self.name = name
        self.series = series
        self.image_url = image_url

        if not date:
            date = datetime.utcnow()
        elif isinstance(date, str):
            date = datetime.fromtimestamp(float(date))

        self.date = date

    def as_dict(self):
        '''Return episode data as properly formatted dictionary.'''
        d = {}

        for field in self.fields:
            d[field] = getattr(self, field)

        d['date'] = self.date.timestamp()

        return d

    def __repr__(self):
        return '''<{self.series}: {self.name} ({self.image_url})>'''.format(self=self)

    def __str__(self):
        return '''{self.series}: {self.name}'''.format(self=self)
