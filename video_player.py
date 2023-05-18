import os.path

from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer, QMediaPlaylist
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QVBoxLayout, QDialog, QStackedWidget, QApplication
import sys


class VideoWindow(QDialog):
    def __init__(self):
        self.filenames = ["start.avi", "tennis.avi", "up_and_down.avi"]

        super(VideoWindow, self).__init__()
        self.setStyleSheet("color: rgb(240, 240, 240); background-color: rgb(16, 16, 16);")

        self.player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.playlist = QMediaPlaylist(self.player)
        self.open_file(self.filenames[0])
        self.open_file(self.filenames[1])
        self.open_file(self.filenames[2])
        # self.playlist.setCurrentIndex(1)
        self.playlist.setPlaybackMode(QMediaPlaylist.CurrentItemInLoop)
        self.player.setPlaylist(self.playlist)
        self.video = QVideoWidget()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.video)
        self.setLayout(self.layout)

        self.player.setVideoOutput(self.video)
        self.player.play()

    def do_exercises(self):
        print("Exercises time")
        # TODO

    def open_file(self, filename):
        self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(os.path.join("", "video", filename))))

    def handle_error(self):
        print("Error: " + self.mediaPlayer.errorString())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = QStackedWidget()
    player = VideoWindow()
    widget.addWidget(player)
    # widget.resize(1400, 1250)
    widget.showFullScreen()
    widget.show()
    sys.exit(app.exec_())
