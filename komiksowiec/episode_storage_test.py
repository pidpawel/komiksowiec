import tempfile
import os.path
from .episode_storage import EpisodeStorage
from .episode import Episode
from datetime import datetime, timedelta


def test_overall():
    with tempfile.TemporaryDirectory() as tmpdir:
        s = EpisodeStorage(cache_dir=tmpdir)

        now = datetime.utcnow()

        eps = [
            Episode('Testowy odcinek', 'Testowa seria', '', now + timedelta(seconds=3)),
            Episode('Testowy odcinek 2', 'Testowa seria', '', now + timedelta(seconds=2)),
            Episode('Testowy odcinek innej serii', 'Testowa seria 2', '', now + timedelta(seconds=1)),
        ]

        for e in eps:
            s.add_episode(e)

        for e, f in zip(eps, s.list_episodes()):
            assert e.name == f.name
            assert e.series == f.series
            assert e.image_url == f.image_url
            assert e.date == f.date

        s.save()
        del s

        s = EpisodeStorage(cache_dir=tmpdir)

        for e, f in zip(eps, s.list_episodes()):
            assert e.name == f.name
            assert e.series == f.series
            assert e.image_url == f.image_url
            assert e.date == f.date


def test_duplicates():
    with tempfile.TemporaryDirectory() as tmpdir:
        s = EpisodeStorage(cache_dir=tmpdir)

        eps = [
            Episode('Testowy odcinek', 'Testowa seria', ''),
            Episode('Testowy odcinek 2', 'Testowa seria', ''),
            Episode('Testowy odcinek innej serii', 'Testowa seria 2', ''),
        ]

        for e in eps:
            s.add_episode(e)

        assert len(s.list_episodes()) == 3

        s.add_episode(Episode('Testowy odcinek', 'Testowa seria', ''))
        assert len(s.list_episodes()) == 3

        s.add_episode(Episode('Testowy odcinek 2', 'Testowa seria', ''))
        s.add_episode(Episode('Testowy odcinek 2', 'Testowa seria', ''))
        s.add_episode(Episode('Testowy odcinek 2', 'Testowa seria', ''))
        assert len(s.list_episodes()) == 3
