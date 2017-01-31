from datetime import datetime


class Episode:
    fields = ['date', 'series', 'name', 'image_url']

    def __init__(self, name, series, image_url, date=None):
        self.name = name
        self.series = series
        self.image_url = image_url

        if not date:
            date = datetime.now()

        self.date = date

    def as_dict(self):
        d = {}

        for field in self.fields:
            d[field] = getattr(self, field)

        return d

    def __repr__(self):
        return '''<{self.series}: {self.name} ({self.image_url})>'''.format(self=self)

    def __str__(self):
        return '''{self.series}: {self.name}'''.format(self=self)
