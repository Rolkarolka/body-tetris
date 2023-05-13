import os.path

from PyQt5.QtCore import  QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QDialog, QPushButton, QHBoxLayout
import sys

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
        game_button.clicked.connect(self.go_to_tetris)
        exercises_button = QPushButton()
        exercises_button.setText("Play Game")
        exercises_button.clicked.connect(self.play_exercises)
        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.addWidget(game_button)
        self.buttons_layout.addWidget(exercises_button)


        self.player.setVideoOutput(self.video)
        self.player.mediaStatusChanged.connect(self.statusChanged)
        self.openFile(self.filename)
        self.player.play()

    def statusChanged(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.layout.addLayout(self.buttons_layout)

    def go_to_tetris(self):
        print("Tetris time")


    def openFile(self, filename):
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(os.path.join(".", "video", filename))))

    def exitCall(self):
        sys.exit(app.exec_())

    def handleError(self):
        print("Error: " + self.mediaPlayer.errorString())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = VideoWindow()
    player.resize(640, 480)
    player.show()
    sys.exit(app.exec_())