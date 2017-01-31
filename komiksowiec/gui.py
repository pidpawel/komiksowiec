from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QGroupBox, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QAction, qApp
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import sys
import os.path
from .episode import Episode
from .crawler import get_crawlers
from .image_cache import ImageCache


class EpisodeWidget(QtWidgets.QWidget):
    def __init__(self, episode=None, parent=None):
        super().__init__(parent)

        self.titleLabel = QtWidgets.QLabel()
        self.seriesLabel = QtWidgets.QLabel()
        self.dateLabel = QtWidgets.QLabel()

        self.episode = None

        if episode:
            self.episode = episode
            self.fillData(episode)

        self._lay_out()
        self._style()

    def _lay_out(self):
        self.mainLayout = QtWidgets.QHBoxLayout()

        self.infoLayout = QtWidgets.QVBoxLayout()
        self.infoLayout.addWidget(self.titleLabel)
        self.infoLayout.addWidget(self.seriesLabel)

        self.mainLayout.addLayout(self.infoLayout)
        self.setLayout(self.mainLayout)

    def _style(self):
        # @TODO style it
        pass

    def fillData(self, episode):
        self.episode = episode

        self.titleLabel.setText(episode.name)
        self.seriesLabel.setText(episode.series)
        # self.dateLabel.setText(episode.date)


class App(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self._init_window()

        self.showMaximized()

        # @TODO https://doc.qt.io/qt-5/qtwidgets-widgets-imageviewer-example.html

    def _init_window(self):
        self.setWindowTitle("Komiksowiec")

        self._init_main_widget()
        self._init_menu()
        self._init_status()
        self._init_docks()

    def _init_main_widget(self):
        self.mainLayout = QtWidgets.QVBoxLayout()

        self.imageLabel = QtWidgets.QLabel()
        self.imageLabel.setAlignment(Qt.AlignCenter)

        base_path = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.abspath(os.path.join(base_path, '..', 'logo.png'))
        self.change_image(QtGui.QPixmap(logo_path))

        self.mainLayout.addWidget(self.imageLabel)

        self.mainWidget = QtWidgets.QWidget()
        self.mainWidget.setLayout(self.mainLayout)

        self.setCentralWidget(self.mainWidget)

    def _init_menu(self):
        exitAction = QAction(QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

    def _init_status(self):
        self.status = self.statusBar()
        self.changeStatus('Starting...')

    def _init_docks(self):
        self.listDock = QtWidgets.QDockWidget('Episode list', self)

        self.listWidget = QtWidgets.QListWidget()
        self.listWidget.itemClicked.connect(self.episodeClicked)
        self.listWidget.currentItemChanged.connect(self.episodeClicked)

        self.cache = ImageCache()
        crawlers = get_crawlers()
        episodes = []

        for crawler_class in crawlers:
            crawler = crawler_class()
            episodes += crawler.crawl()

        for episode in episodes:
            self.cache.cache_image(episode.image_url)

            episodeWidget = EpisodeWidget(episode)
            episodeWidgetItem = QtWidgets.QListWidgetItem()
            episodeWidgetItem.setSizeHint(episodeWidget.sizeHint())
            self.listWidget.addItem(episodeWidgetItem)
            self.listWidget.setItemWidget(episodeWidgetItem, episodeWidget)

        self.listDock.setWidget(self.listWidget)
        self.addDockWidget(Qt.RightDockWidgetArea, self.listDock)

    def change_image(self, pixmap):
        self.imageLabel.setPixmap(pixmap)

    def changeStatus(self, text):
        self.status.showMessage(text)

    def episodeClicked(self, item):
        widget = self.listWidget.itemWidget(item)
        self.change_image(QtGui.QPixmap(self.cache.get_image_path(widget.episode.image_url)))


def main():
    app = QtWidgets.QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
