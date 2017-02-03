Developer guide
===============

This part of the documentation is intended to list and describe all classes and methods used in application.
One may be able to extend the functionality of this program using this information.
Most of it can be found in the application code, but here classes/functions are presented in some logical way.

.. toctree::
   :maxdepth: 2


Libraries
---------

Crawlers are built around requests (and responses for testing) and lxml libraries.
GUI is made with PyQt5.


Tests
-----

All tests are done with pytest::

    python3 -m pytest -v


Komiksowiec
-----------

.. automodule:: komiksowiec.komiksowiec
   :members:
   :undoc-members:
   :inherited-members:
   :special-members: __init__


SettingsContainer
-----------------

.. automodule:: komiksowiec.settings_container
   :members:
   :undoc-members:
   :inherited-members:
   :special-members: __init__


Crawler
-------

.. automodule:: komiksowiec.crawler
   :members:
   :undoc-members:
   :inherited-members:


Episode
-------

.. automodule:: komiksowiec.episode
   :members:
   :undoc-members:
   :inherited-members:
   :special-members: __init__


EpisodeStorage
--------------

.. automodule:: komiksowiec.episode_storage
   :members:
   :undoc-members:
   :inherited-members:
   :special-members: __init__


ImageCache
----------

.. automodule:: komiksowiec.image_cache
   :members:
   :undoc-members:
   :inherited-members:
   :special-members: __init__

