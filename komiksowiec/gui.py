from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QGroupBox, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QAction, qApp
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import sys
import os.path
from .komiksowiec import Komiksowiec


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
        self.komiksowiec = Komiksowiec()

        self._init_window()

        self.showMaximized()
        # @TODO https://doc.qt.io/qt-5/qtwidgets-widgets-imageviewer-example.html

    def _init_window(self):
        self.setWindowTitle("Komiksowiec")

        self._init_main_widget()
        self._init_docks()

        self._init_actions()
        self._init_menu()
        self._init_toolbar()

        self._init_status()

    def _init_main_widget(self):
        self.mainLayout = QtWidgets.QVBoxLayout()

        self.imageLabel = QtWidgets.QLabel()
        self.imageLabel.setAlignment(Qt.AlignCenter)

        self.change_image(None)

        self.mainLayout.addWidget(self.imageLabel)

        self.mainWidget = QtWidgets.QWidget()
        self.mainWidget.setLayout(self.mainLayout)

        self.setCentralWidget(self.mainWidget)

    def _init_actions(self):
        # https://standards.freedesktop.org/icon-naming-spec/icon-naming-spec-latest.html
        self.exitAction = QAction(QIcon.fromTheme('application-exit'), 'Exit')
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip('Exit application')
        self.exitAction.triggered.connect(qApp.quit)

        self.updateAction = QAction(QIcon.fromTheme('view-refresh'), 'Update')
        self.updateAction.setShortcut('Ctrl+Q')
        self.updateAction.setStatusTip('Exit application')
        self.updateAction.triggered.connect(self.update)

    def _init_menu(self):
        menubar = self.menuBar()

        fileMenu = menubar.addMenu('File')
        fileMenu.addAction(self.exitAction)

    def _init_toolbar(self):
        self.toolbar = self.addToolBar('Toolbar')
        self.toolbar.addAction(self.exitAction)
        self.toolbar.addAction(self.updateAction)

    def _init_status(self):
        self.status = self.statusBar()
        self.changeStatus('Starting...')

    def _init_docks(self):
        self.listDock = QtWidgets.QDockWidget('Episode list', self)

        self.listWidget = QtWidgets.QListWidget()
        self.listWidget.itemClicked.connect(self.episodeClicked)
        self.listWidget.currentItemChanged.connect(self.episodeClicked)

        self.listDock.setWidget(self.listWidget)
        self.addDockWidget(Qt.RightDockWidgetArea, self.listDock)

        self.refresh_list()

    def refresh_list(self):
        self.listWidget.clear()

        for episode in self.komiksowiec.get_comics():
            episodeWidget = EpisodeWidget(episode)
            episodeWidgetItem = QtWidgets.QListWidgetItem()
            episodeWidgetItem.setSizeHint(episodeWidget.sizeHint())
            self.listWidget.addItem(episodeWidgetItem)
            self.listWidget.setItemWidget(episodeWidgetItem, episodeWidget)

    def change_image(self, pixmap):
        if not pixmap:
            base_path = os.path.dirname(os.path.abspath(__file__))
            logo_path = os.path.abspath(os.path.join(base_path, '..', 'logo.png'))
            self.imageLabel.setPixmap(QtGui.QPixmap(logo_path))
            return

        self.imageLabel.setPixmap(pixmap)

    def changeStatus(self, text):
        self.status.showMessage(text)

    def episodeClicked(self, item):
        if not item:
            self.change_image(None)
            return

        widget = self.listWidget.itemWidget(item)
        image_path = self.komiksowiec.image_cache.get_image_path(widget.episode.image_url)
        self.change_image(QtGui.QPixmap(image_path))

    def update(self):
        self.komiksowiec.update()
        self.refresh_list()
        self.listWidget.setCurrentRow(0)


def main():
    app = QtWidgets.QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
