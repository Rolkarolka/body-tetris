import os.path

from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtCore import *
from pathlib import Path

import sys

app = QApplication(sys.argv)
w = QVideoWidget()
w.resize(300, 300)
w.move(0, 0)
w.show()

player = QMediaPlayer()
player.setMedia(QMediaContent(QUrl.fromLocalFile(os.path.abspath(Path("video", "start.avi")))))
player.setVideoOutput(w)

player.play()

sys.exit(app.exec_())