import os
import sys
from PyQt5 import QtWidgets, QtCore, QtGui

# Initiate values
filename = "D:/PL_GUI/cat.jpg"
start_point = [0, 0]
end_point = [0, 0]

lightgray_stylesheet = "border:0;\nbackground-color: rgb(221, 221, 221);"

class image_editor(object):

    # Set up image editor
    def setupUi(self, new_widget):
        # Initiate new_widget to this new object
        new_widget.setObjectName("new_widget")

        new_widget.setMinimumSize(QtCore.QSize(1280, 720))
        new_widget.setMaximumSize(QtCore.QSize(1280, 720))
        new_widget.setStyleSheet(lightgray_stylesheet)

        self.centralwidget = QtWidgets.QWidget(new_widget)
        self.centralwidget.setObjectName("centralwidget")

        # Image editor
        self.image_viewer = QtWidgets.QLabel(self.centralwidget)
        self.image_viewer.setGeometry(QtCore.QRect(30, 80, 960, 540))
        self.image_viewer.setMaximumSize(QtCore.QSize(960, 540))
        self.display_image()

        # Initiate mouse point
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()

        new_widget.setCentralWidget(self.centralwidget)

    # Use to update the image to the image editor/image canvas
    def display_image(self):
        background = QtGui.QPixmap(filename)
        scaled_background = background.scaled(960, 540)
        self.image_viewer.setPixmap(scaled_background)

    # Redefine Paint event
    def paintEvent(self, event):
        qp = QtGui.QPainter()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 0, 70))
        qp.setBrush(brush)
        pen = QtGui.QPen(QtGui.QColor(255, 255, 0, 100))
        qp.setPen(pen)
        qp.drawRect(QtCore.QRect(self.begin, self.end))

    # Redefine mouse press event
    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = event.pos()
        # Pass starting point position to a temp variable
        start_point[0] = event.pos().x()
        start_point[1] = event.pos().y()
        # Debug
        print("Start point = {}, {}".format(start_point[0], start_point[1]))
        self.update()

    # Redefine mouse move event
    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    # Redefine mouse release event
    def mouseReleaseEvent(self, event):
        self.begin = event.pos()
        self.end = event.pos()
        # Pass ending point position to a temp variable
        end_point[0] = event.pos().x()
        end_point[1] = event.pos().y()
        # Debug
        print("End point = {}, {}".format(end_point[0], end_point[1]))
        self.update()
# ----------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    new_widget = QtWidgets.QMainWindow()
    ui = image_editor()
    ui.setupUi(new_widget)
    new_widget.show()
    sys.exit(app.exec_())