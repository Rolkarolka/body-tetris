import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QHBoxLayout, QWidget, QVBoxLayout

class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.gameButton = QPushButton()
        self.gameButton.setText("Play game")
        self.gameButton.clicked.connect(self.gotoScreen2)
        layout = QVBoxLayout()
        layout.addWidget(self.gameButton)
        wid = QWidget(self)
        wid.setLayout(layout)

    def gotoScreen2(self):
        screen2=Screen2()
        widget.addWidget(screen2)
        widget.setCurrentIndex(widget.currentIndex()+1)

class Screen2(QDialog):
    def __init__(self):
        super(Screen2, self).__init__()
        self.returnButton = QPushButton()
        self.returnButton.setText("Return")
        self.returnButton.clicked.connect(self.gotoScreen1)
        layout = QVBoxLayout()
        layout.addWidget(self.returnButton)
        wid = QWidget(self)
        wid.setLayout(layout)

    def gotoScreen1(self):
        main_window=MainWindow()
        widget.addWidget(main_window)
        widget.setCurrentIndex(widget.currentIndex()+1)

app = QApplication(sys.argv)
widget=QtWidgets.QStackedWidget()
main_window = MainWindow()
widget.addWidget(main_window)
widget.resize(640, 480)
widget.show()
sys.exit(app.exec_())