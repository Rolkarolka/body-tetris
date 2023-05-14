
from PyQt5.QtWidgets import QDesktopWidget, QHBoxLayout
from PyQt5.QtCore import QBasicTimer
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QDialog, QFrame

from tetris_model import BOARD_DATA, Shape
from semaphore import Move, PoseExtractor


class Tetris(QDialog):
    def __init__(self, get_pose=None, return_screen=lambda: print("Implement return fun")):
        super(Tetris, self).__init__()
        self.isStarted = False
        self.isPaused = False
        self.get_pose = get_pose
        self.lastShape = Shape.shapeNone
        self.return_screen=return_screen

        self.gridSize = 22
        self.speed = 600
        self.pose_speed = 100

        self.timer = QBasicTimer()
        self.pose_timer = QBasicTimer()
        # self.setFocusPolicy(Qt.StrongFocus)

        board_layout = QHBoxLayout()

        self.tboard = Board(self, self.gridSize)
        self.sidePanel = SidePanel(self, self.gridSize)
        board_layout.addWidget(self.tboard)
        board_layout.addWidget(self.sidePanel)

        self.setLayout(board_layout)
        self.start()
        self.center()

        self.poseExtractor = PoseExtractor()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)

    def start(self):
        if self.isPaused:
            return

        self.isStarted = True
        self.tboard.score = 0
        BOARD_DATA.clear()


        BOARD_DATA.createNewPiece()
        self.timer.start(self.speed, self)
        self.pose_timer.start(self.pose_speed, self)

    def pause(self):
        if not self.isStarted:
            return

        self.isPaused = not self.isPaused

        if self.isPaused:
            self.timer.stop()
        else:
            self.timer.start(self.speed, self)
            self.pose_timer.start(self.pose_timer, self)

        self.update_window()

    def update_window(self):
        self.tboard.update_data()
        self.sidePanel.update_data()
        self.update()

    def timerEvent(self, event):
        if event.timerId() == self.pose_timer.timerId():
            self.get_move()

        if event.timerId() == self.timer.timerId():
            lines, result = BOARD_DATA.moveDown()
            if not result:
                self.pause()
                self.return_screen()
                # self.__init__(self.get_pose)
            self.tboard.score += lines
            if self.lastShape != BOARD_DATA.currentShape:
                 self.lastShape = BOARD_DATA.currentShape
            self.update_window()
        else:
            super(Tetris, self).timerEvent(event)

    def get_move(self):
        if not self.isStarted or BOARD_DATA.currentShape == Shape.shapeNone:
            return

        # move = self.get_pose()
        move = self.poseExtractor.get_pose()
        if move is not None:
            print(move) # TODO
        if self.isPaused:
            return
        elif move == Move.LEFT:
            BOARD_DATA.moveLeft()
        elif move == Move.RIGHT:
            BOARD_DATA.moveRight()
        elif move == Move.JUMP:
            BOARD_DATA.rotateLeft()
        self.update_window()


def draw_square(painter, x, y, val, s):
    color_table = [0x000000, 0xCC6666, 0x66CC66, 0x6666CC,
                  0xCCCC66, 0xCC66CC, 0x66CCCC, 0xDAAA00]

    if val == 0:
        return

    color = QColor(color_table[val])
    painter.fillRect(x + 1, y + 1, s - 2, s - 2, color)

    painter.setPen(color.lighter())
    painter.drawLine(x, y + s - 1, x, y)
    painter.drawLine(x, y, x + s - 1, y)

    painter.setPen(color.darker())
    painter.drawLine(x + 1, y + s - 1, x + s - 1, y + s - 1)
    painter.drawLine(x + s - 1, y + s - 1, x + s - 1, y + 1)


class SidePanel(QFrame):
    def __init__(self, parent, gridSize):
        super().__init__(parent)
        self.setFixedSize(gridSize * 5, gridSize * BOARD_DATA.height)
        self.move(gridSize * BOARD_DATA.width, 0)
        self.gridSize = gridSize

    def update_data(self):
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        min_x, max_x, min_y, max_y = BOARD_DATA.nextShape.getBoundingOffsets(0)

        dy = 3 * self.gridSize
        dx = (self.width() - (max_x - min_x) * self.gridSize) / 2

        val = BOARD_DATA.nextShape.shape
        for x, y in BOARD_DATA.nextShape.getCoords(0, 0, -min_y):
            draw_square(painter, x * self.gridSize + dx, y * self.gridSize + dy, val, self.gridSize)


class Board(QFrame):
    speed = 10

    def __init__(self, parent, gridSize):
        super().__init__(parent)
        self.setFixedSize(gridSize * BOARD_DATA.width, gridSize * BOARD_DATA.height)
        self.gridSize = gridSize
        self.score = 0
        BOARD_DATA.clear()

    def paintEvent(self, event):
        painter = QPainter(self)

        # Draw backboard
        for x in range(BOARD_DATA.width):
            for y in range(BOARD_DATA.height):
                val = BOARD_DATA.getValue(x, y)
                draw_square(painter, x * self.gridSize, y * self.gridSize, val, self.gridSize)

        # Draw current shape
        for x, y in BOARD_DATA.getCurrentShapeCoord():
            val = BOARD_DATA.currentShape.shape
            draw_square(painter, x * self.gridSize, y * self.gridSize, val, self.gridSize)

        # Draw a border
        painter.setPen(QColor(0x777777))
        painter.drawLine(self.width()-1, 0, self.width()-1, self.height())
        painter.setPen(QColor(0xCCCCCC))
        painter.drawLine(self.width(), 0, self.width(), self.height())

    def update_data(self):
        self.update()
