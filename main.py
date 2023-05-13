from queue import Queue
from threading import Thread

from semaphore import PoseExtractor
from tetris_game import Tetris
from PyQt5.QtWidgets import QApplication
import sys

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
    app = QApplication([])
    tetris = Tetris(lambda: queue.get(block=False) if not queue.empty() else None)
    total_end = True
    sys.exit(app.exec_())


if __name__ == '__main__':
    queue = Queue()
    producer = Thread(target=produce_pose, args=(queue,))
    producer.start()
    consumer = Thread(target=consume_pose, args=(queue,))
    consumer.start()
    producer.join()
    consumer.join()




