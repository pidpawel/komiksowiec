import tempfile
import os.path
from .settings_container import SettingsContainer


def test_overall():
    with tempfile.TemporaryDirectory() as tmpdir:
        s = SettingsContainer(cache_dir=tmpdir)

        s.set('test', 1)
        assert s.get('test') == 1

        s.register_default('test2', 3)
        assert s.get('test2') == 3  # from defaults
        assert s.get('test2') == 3  # from settings

        s.save()
        del s

        s = SettingsContainer(cache_dir=tmpdir)  # assuming reread
        assert s.get('test') == 1
        assert s.get('test2') == 3
