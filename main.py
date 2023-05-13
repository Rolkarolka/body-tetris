from queue import Queue
from threading import Thread

from semaphore import PoseExtractor
from tetris_game import Tetris
from PyQt5.QtWidgets import QApplication
import sys
import os.path

from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtCore import *
from pathlib import Path

total_end = False
def produce_pose(queue):
    global total_end
    poseExtractor = PoseExtractor()
    while poseExtractor.is_end() is False or total_end is True:
        m = poseExtractor.get_pose()
        if m is not None:
            print(m)
            queue.put(m)
    total_end = True

def consume_pose(queue):
    global total_end
    tetris = Tetris(lambda: queue.get(block=False) if not queue.empty() else None)
    total_end = True


if __name__ == '__main__':
    app = QApplication([])
    # run tetris
    queue = Queue()
    producer = Thread(target=produce_pose, args=(queue,))
    producer.start()
    consumer = Thread(target=consume_pose, args=(queue,))
    consumer.start()
    producer.join()
    consumer.join()
    sys.exit(app.exec_())



