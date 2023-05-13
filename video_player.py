# PyQt5 Video player
#!/usr/bin/env python
import os.path

from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget)
from PyQt5.QtWidgets import QMainWindow,QWidget, QPushButton, QAction, QDialog
from PyQt5.QtGui import QIcon
import sys

class VideoWindow(QDialog):

    def __init__(self):
        super(VideoWindow, self).__init__()

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        videoWidget = QVideoWidget()

        self.moveButton = QPushButton()
        self.moveButton.setText("Play game")
        self.moveButton.clicked.connect(self.hello)
        controlLayout = QHBoxLayout()
        controlLayout.addWidget(self.moveButton)
        controlLayout.addWidget(videoWidget)
        
        # Create exit action
        exitAction = QAction(QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.exitCall)


        # Create a widget for window contents
        wid = QWidget(self)
        # self.setCentralWidget(wid)

        layout = QVBoxLayout()
        # layout.addWidget(videoWidget)
        layout.addLayout(controlLayout)

        # Set widget to contain window contents
        wid.setLayout(layout)

        self.mediaPlayer.setVideoOutput(videoWidget)

        self.openFile("start.avi")
        self.play()

    def openFile(self, filename):
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(os.path.join(".", "video", filename))))

    def exitCall(self):
        sys.exit(app.exec_())

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()
    def hello(self):
        print("hello")
    def handleError(self):
        print("Error: " + self.mediaPlayer.errorString())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = VideoWindow()
    player.resize(640, 480)
    player.show()
    sys.exit(app.exec_())