import os.path
from queue import Queue

from PyQt5.QtCore import  QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QVBoxLayout, QDialog, QPushButton, QHBoxLayout, QStackedWidget, QApplication
import sys

from tetris_game import Tetris
class VideoWindow(QDialog):

    def __init__(self, filename="start.avi"):
        self.filename = filename

        super(VideoWindow, self).__init__()

        self.player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.video = QVideoWidget()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.video)
        self.setLayout(self.layout)

        game_button = QPushButton()
        game_button.setText("Play Game")
        game_button.clicked.connect(play_tetris)
        exercises_button = QPushButton()
        exercises_button.setText("Do exercises")
        exercises_button.clicked.connect(self.do_exercises)
        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.addWidget(game_button)
        self.buttons_layout.addWidget(exercises_button)

        self.player.setVideoOutput(self.video)
        self.player.mediaStatusChanged.connect(self.status_changed)
        self.open_file(self.filename)
        self.player.play()

    def status_changed(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.layout.addLayout(self.buttons_layout)

    def do_exercises(self):
        print("Exercises time")
        # TODO

    def open_file(self, filename):
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(os.path.join("", "video", filename))))

    def handle_error(self):
        print("Error: " + self.mediaPlayer.errorString())

def go_to_video_player():
    main_window = VideoWindow("up_and_down.avi")
    widget.addWidget(main_window)
    widget.setCurrentIndex(widget.currentIndex() + 1)

def play_tetris():
    queue = Queue()
    tetris = Tetris(
        lambda: queue.get(block=False) if not queue.empty() else None,
        lambda: go_to_video_player()
    )
    widget.addWidget(tetris)
    widget.setCurrentIndex(widget.currentIndex() + 1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = QStackedWidget()
    player = VideoWindow()
    widget.addWidget(player)
    widget.resize(640, 480)
    # widget.showFullScreen()
    widget.show()
    sys.exit(app.exec_())