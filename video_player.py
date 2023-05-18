import os.path

from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QVBoxLayout, QDialog, QStackedWidget, QApplication
import sys

from tetris_game import Tetris


class VideoWindow(QDialog):
    def __init__(self, filename, play_next):
        self.filename = filename
        self.play_next = play_next

        super(VideoWindow, self).__init__()
        self.setStyleSheet("color: rgb(240, 240, 240); background-color: rgb(16, 16, 16);")

        self.player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.video = QVideoWidget()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.video)
        self.setLayout(self.layout)

        self.player.setVideoOutput(self.video)
        self.player.mediaStatusChanged.connect(self.status_changed)
        self.open_file(self.filename)

    def status_changed(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.play_next()

    def open_file(self, filename):
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(os.path.abspath(os.path.join("", "video", filename)))))

    def handle_error(self):
        print("Error: " + self.mediaPlayer.errorString())

    def run(self):
        self.player.play()


class Youtine:
    def __init__(self):
        formatt = "avi"
        self.widget = QStackedWidget()

        self.player_start = VideoWindow('start.' + formatt, lambda: self.play(1))
        self.tetris = Tetris(lambda: self.play(2))
        self.player_end = VideoWindow('up_and_down.' + formatt, lambda: self.play(0))

        self.widget.addWidget(self.player_start)
        self.widget.addWidget(self.tetris)
        self.widget.addWidget(self.player_end)
        # self.widget.resize(1400, 1250)

    def show(self):
        assert self.widget.currentIndex() == 0
        self.widget.showFullScreen()
        self.run(0)

    def run(self, index):
        if index == 0:
            self.player_start.run()
        elif index == 1:
            self.tetris.run()
        elif index == 2:
            self.player_end.run()

    def play(self, index):
        self.widget.setCurrentIndex(index)
        self.run(index)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    Youtine().show()
    sys.exit(app.exec_())
