from PyQt5 import QtWidgets, uic
import sys
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('image-viewer.ui', self)

        self.title = "Image Viewer"
        self.setWindowTitle(self.title)

        self.load_1.clicked.connect(self.load_frame_1)
        self.load_2.clicked.connect(self.load_frame_2)
        self.reset_b.clicked.connect(self.reset_frame)
        self.show()

    def load_frame_1(self):
        pixmap = QPixmap('cat.jpg')
        self.image_display.setPixmap(pixmap)
        self.image_display.setScaledContents(True)

    def load_frame_2(self):
        pixmap = QPixmap('E:\[PERSONALIZE] Pictures\Wallpaper\cute-cat-in-snow.jpg')
        self.image_display_2.setPixmap(pixmap)
        self.image_display_2.setScaledContents(True)

    def reset_frame(self):
        print("reset")
        pixmap = QPixmap(None)
        self.image_display.setPixmap(pixmap)
        self.image_display_2.setPixmap(pixmap)


app = QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec_())