from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QRegExpValidator
from PyQt5.QtCore import Qt, QRegExp, QTimer
import sys
import os.path
import requests
from .komiksowiec import Komiksowiec


class EpisodeWidget(QtWidgets.QWidget):
    # https://stackoverflow.com/questions/25187444/pyqt-qlistwidget-custom-items
    def __init__(self, episode=None, parent=None):
        super().__init__(parent)

        self.titleLabel = QtWidgets.QLabel()
        self.seriesLabel = QtWidgets.QLabel()

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
        self.titleLabel.setStyleSheet('font-weight: bold;')

    def fillData(self, episode):
        self.episode = episode

        self.titleLabel.setText(episode.name)
        self.seriesLabel.setText(episode.series)


class SettingsDialog(QtWidgets.QDialog):
    def __init__(self, komiksowiec, parent=None):
        super().__init__(parent)
        self.komiksowiec = komiksowiec

        self.setWindowTitle('Settings')

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.digitRe = QRegExp()
        self.digitRe.setPattern('[0-9]+')

        self.intervalLayout = QHBoxLayout()
        self.intervalLabel = QLabel('Interval')
        self.intervalInput = QLineEdit(str(self.komiksowiec.settings.get('update_interval')))
        self.intervalInput.setValidator(QRegExpValidator(self.digitRe))
        self.intervalLayout.addWidget(self.intervalLabel)
        self.intervalLayout.addWidget(self.intervalInput)
        self.layout.addLayout(self.intervalLayout)

        self.buttonsLayout = QHBoxLayout()
        self.cancelButton = QPushButton('Cancel')
        self.cancelButton.clicked.connect(self.cancel)
        self.saveButton = QPushButton('Save')
        self.saveButton.clicked.connect(self.save)
        self.buttonsLayout.addWidget(self.cancelButton)
        self.buttonsLayout.addWidget(self.saveButton)
        self.layout.addLayout(self.buttonsLayout)

    def cancel(self):
        self.close()

    def save(self):
        settings = self.komiksowiec.settings
        settings.set('update_interval', int(self.intervalInput.text()))
        settings.save()
        self.close()


class App(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.komiksowiec = Komiksowiec(log_callback=self.changeStatus)
        self.settingsDialog = SettingsDialog(komiksowiec=self.komiksowiec)

        self._init_window()

        self.showMaximized()
        # https://doc.qt.io/qt-5/qtwidgets-widgets-imageviewer-example.html
        # https://pythonspot.com/en/pyqt5/

        self.updateTimer = QTimer()
        self.updateTimer.timeout.connect(self.update)
        self.updateTimer.start(1000 * 60 * self.komiksowiec.settings.get('update_interval'))

        self.update()

    def _init_window(self):
        self.setWindowTitle("Komiksowiec")

        # http://zetcode.com/gui/pyqt5/menustoolbars/
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
        self.updateAction.setShortcut('Ctrl+U')
        self.updateAction.setStatusTip('Update comics')
        self.updateAction.triggered.connect(self.update)

        self.settingsAction = QAction(QIcon.fromTheme('emblem-system'), 'Settings')
        self.settingsAction.setShortcut('Ctrl+S')
        self.settingsAction.setStatusTip('Open settings')
        self.settingsAction.triggered.connect(self.openSettings)

    def _init_menu(self):
        menubar = self.menuBar()

        fileMenu = menubar.addMenu('File')
        fileMenu.addAction(self.exitAction)

    def _init_toolbar(self):
        self.toolbar = self.addToolBar('Toolbar')
        self.toolbar.addAction(self.exitAction)
        self.toolbar.addAction(self.updateAction)
        self.toolbar.addAction(self.settingsAction)

    def _init_status(self):
        self.status = self.statusBar()
        self.changeStatus('Starting...')

    def _init_docks(self):
        # https://www.tutorialspoint.com/pyqt/pyqt_qdockwidget.htm
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
        print(text)
        self.status.showMessage(text)

    def episodeClicked(self, item):
        if not item:
            self.change_image(None)
            return

        widget = self.listWidget.itemWidget(item)
        image_path = self.komiksowiec.image_cache.get_image_path(widget.episode.image_url)
        self.change_image(QtGui.QPixmap(image_path))

    def update(self):
        try:
            self.komiksowiec.update()
        except requests.exceptions.RequestException:
            self.changeStatus('Could not connect to the network')
        else:
            self.refresh_list()
            # self.listWidget.setCurrentRow(0)

    def openSettings(self):
        self.settingsDialog.exec_()


def main():
    app = QtWidgets.QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
