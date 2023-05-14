# from queue import Queue
#
# from semaphore import PoseExtractor
# from tetris_game import Tetris
# import sys
#
# from PyQt5.QtWidgets import QStackedWidget, QApplication
#
# def produce_pose(queue):
#     global total_end
#     poseExtractor = PoseExtractor()
#     while poseExtractor.is_end() is False:
#         m = poseExtractor.get_pose()
#         if m is not None:
#             print(m)
#             queue.put(m)
#
# def consume_pose(queue):
#     widget = QStackedWidget()
#     tetris = Tetris(lambda: queue.get(block=False) if not queue.empty() else None)
#     widget.addWidget(tetris)
#     widget.resize(640, 480)
#     widget.show()
#
#
# if __name__ == '__main__':
#     # run tetris
#     app = QApplication([])
#     queue = Queue()
#     # producer = Thread(target=produce_pose, args=(queue,))
#     # consumer = Thread(target=consume_pose, args=(queue,))
#     #
#     # producer.start()
#     # consumer.start()
#     # producer.join()
#     # consumer.join()
#     widget = QStackedWidget()
#     tetris = Tetris(lambda: queue.get(block=False) if not queue.empty() else None)
#     widget.addWidget(tetris)
#     widget.resize(640, 480)
#     widget.show()
#
#     sys.exit(app.exec_())