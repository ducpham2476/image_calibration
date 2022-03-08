# Import packages
import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QHBoxLayout, QVBoxLayout, QPushButton,\
    QSizePolicy
from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.QtGui import QPixmap, QPainter, QBrush, QPen, QColor


# Initiate values
filename = "D:/PL_GUI/cat.jpg"
start_point = [0, 0]
end_point = [0, 0]

teal_label_stylesheet = "color: rgb(91, 206, 206);\nbackground-color: rgb(255, 255, 255);"

lightgray_stylesheet = "border:0;\nbackground-color: rgb(221, 221, 221);"

darkgray_stylesheet = "background-color: rgb(135, 135, 135);\ncolor: rgb(255, 255, 255);"

yellow_button_stylesheet = "QPushButton{\n"\
                           "   background-color: rgb(234, 189, 75);\n"\
                           "   color: rgb(255, 255, 255);}\n"\
                           "QPushButton:hover{\n"\
                           "   background-color: rgb(255, 206, 82);}\n"\
                           "QPushButton:pressed{\n"\
                           "   background-color: rgb(179, 145, 57);}"

teal_button_stylesheet = "QPushButton{\n"\
                          "   background-color: rgb(91, 206, 206);\n"\
                          "   color: rgb(255, 255, 255);}\n"\
                          "QPushButton:hover{\n"\
                          "   background-color: rgb(108, 245, 245);}\n"\
                          "QPushButton:pressed{\n"\
                          "   background-color: rgb(51, 153, 150);}"

gray_button_stylesheet = "QPushButton{\n"\
                         "  background-color:rgb(135, 135, 135);\n"\
                         "  color: rgb(255, 255, 255);}\n"\
                         "QPushButton:hover{\n"\
                         "  background-color:rgb(180, 180, 180);}\n"\
                         "QPushButton:pressed{\n"\
                         "  background-color:rgb(86, 86, 86);}\n"

red_button_stylesheet = "QPushButton{\n" \
                        "  background-color:rgb(229, 95, 95);\n"\
                        "  color: rgb(255, 255, 255);}\n"\
                        "QPushButton:hover{\n"\
                        "  background-color:rgb(255, 106, 106);}\n"\
                        "QPushButton:pressed{\n"\
                        "  background-color:rgb(167, 69, 69);}\n"

# Define new objects
class Ui_MainWindow(object):

    def setupUi(self, MainWindow):

        # Create MainWindow
        MainWindow.setObjectName("MainWindow")

        MainWindow.resize(1280, 720)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(1280, 720))
        MainWindow.setMaximumSize(QtCore.QSize(1280, 720))
        MainWindow.setStyleSheet(lightgray_stylesheet)

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # self.image_disp = draw_on_qlabel()

        # Horizontal Layout 1: Save Landmark and Parking Lot Buttons
        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 630, 430, 80))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")

        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")

        # Save landmark button
        self.savelm_B = QPushButton(self.horizontalLayoutWidget)
        self.savelm_B.setMaximumSize(QtCore.QSize(200, 40))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.savelm_B.setFont(font)
        self.savelm_B.setStyleSheet(yellow_button_stylesheet)
        self.savelm_B.setObjectName("savelm_B")
        self.horizontalLayout_5.addWidget(self.savelm_B)

        # Save parking lot button
        self.saveplot_B = QPushButton(self.horizontalLayoutWidget)
        self.saveplot_B.setMaximumSize(QtCore.QSize(200, 40))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.saveplot_B.setFont(font)
        self.saveplot_B.setStyleSheet(teal_button_stylesheet)
        self.saveplot_B.setObjectName("saveplot_B")
        self.horizontalLayout_5.addWidget(self.saveplot_B)


        #  Horizontal layout 2: With Back and Next button
        self.horizontalLayoutWidget_2 = QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(1010, 630, 261, 80))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")

        # Back button
        self.back_B = QPushButton(self.horizontalLayoutWidget_2)
        self.back_B.setMaximumSize(QtCore.QSize(100, 40))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.back_B.setFont(font)
        self.back_B.setStyleSheet(gray_button_stylesheet)
        self.back_B.setObjectName("back_B")
        self.horizontalLayout_6.addWidget(self.back_B)

        # Next button
        self.next_B = QPushButton(self.horizontalLayoutWidget_2)
        self.next_B.setMaximumSize(QtCore.QSize(100, 40))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.next_B.setFont(font)
        self.next_B.setStyleSheet(teal_button_stylesheet)
        self.next_B.setObjectName("next_B")
        self.horizontalLayout_6.addWidget(self.next_B)

        # List Widget: Use to display data
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(1020, 80, 231, 270))
        self.listWidget.setMaximumSize(QtCore.QSize(240, 270))
        self.listWidget.setStyleSheet(darkgray_stylesheet)
        self.listWidget.setObjectName("listWidget")
        self.data_stored_label = QtWidgets.QLabel(self.centralwidget)
        self.data_stored_label.setGeometry(QtCore.QRect(1020, 40, 231, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.data_stored_label.setFont(font)
        self.data_stored_label.setStyleSheet("color: rgb(75, 75, 75);")
        self.data_stored_label.setAlignment(QtCore.Qt.AlignCenter)
        self.data_stored_label.setObjectName("data_stored_label")

        # Vertical layout: Undo, Redo and Reset Button
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(1020, 360, 101, 171))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(10)
        self.verticalLayout_3.setObjectName("verticalLayout_3")

        # Undo button
        self.undo_B = QPushButton(self.verticalLayoutWidget)
        self.undo_B.setMaximumSize(QtCore.QSize(100, 40))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.undo_B.setFont(font)
        self.undo_B.setStyleSheet(gray_button_stylesheet)
        self.undo_B.setObjectName("undo_B")
        self.verticalLayout_3.addWidget(self.undo_B)

        # Redo button
        self.redo_B = QPushButton(self.verticalLayoutWidget)
        self.redo_B.setMaximumSize(QtCore.QSize(100, 40))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.redo_B.setFont(font)
        self.redo_B.setStyleSheet(teal_button_stylesheet)
        self.redo_B.setObjectName("redo_B")
        self.verticalLayout_3.addWidget(self.redo_B)

        # Reset Button
        self.reset_B = QPushButton(self.verticalLayoutWidget)
        self.reset_B.setMaximumSize(QtCore.QSize(100, 40))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.reset_B.setFont(font)
        self.reset_B.setStyleSheet(red_button_stylesheet)
        self.reset_B.setObjectName("reset_B")
        self.verticalLayout_3.addWidget(self.reset_B)


        self.define_parking_lot_label = QtWidgets.QLabel(self.centralwidget)
        self.define_parking_lot_label.setGeometry(QtCore.QRect(460, 20, 410, 40))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.define_parking_lot_label.setFont(font)
        self.define_parking_lot_label.setStyleSheet(teal_label_stylesheet)
        self.define_parking_lot_label.setAlignment(QtCore.Qt.AlignCenter)
        self.define_parking_lot_label.setObjectName("define_parking_lot_label")

        # Load button
        self.load_B = QPushButton(self.centralwidget)
        self.load_B.setGeometry(QtCore.QRect(30, 20, 99, 40))
        self.load_B.setMaximumSize(QtCore.QSize(100, 40))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.load_B.setFont(font)
        self.load_B.setStyleSheet(teal_button_stylesheet)
        self.load_B.setObjectName("load_B")

        # Image canvas display
        # self.image_disp.setGeometry(QtCore.QRect(30, 80, 960, 540))
        #
        # sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # self.image_disp.setSizePolicy(sizePolicy)
        # self.image_disp.setMinimumSize(QtCore.QSize(960, 540))
        # self.image_disp.setMaximumSize(QtCore.QSize(960, 540))
        #
        # canvas = QPixmap(960, 540)
        # canvas.fill(QColor('white'))
        #
        # self.image_disp.setPixmap(canvas)
        # self.begin = QPoint()
        # self.end = QPoint()

        # font = QtGui.QFont()
        # font.setFamily("Montserrat")
        # font.setPointSize(14)
        # font.setBold(True)
        # font.setItalic(True)
        # font.setWeight(75)
        # self.image_disp.setFont(font)
        # self.image_disp.setStyleSheet(darkgray_stylesheet)
        # self.image_disp.setAlignment(QtCore.Qt.AlignCenter)
        # self.image_disp.setObjectName("image_disp")

        # self.image_disp.getGeometry(QRect(30, 80, 960, 540))
        # sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # self.image_disp.setSizePolicy(sizePolicy)
        # self.image_disp.setMaximumSize(QtCore.QSize(960, 540))
        # self.image_disp.setMinimumSize(QtCore.QSize(960, 540))

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1280, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # RetranslateUi
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.begin = QPoint()
        self.end = QPoint()

    def paintEvent(self, event):
        qp = QPainter(self)
        pixmap = QPixmap(960, 540)
        pixmap.fill(QColor('white'))
        qp.drawPixmap(self.rect(), pixmap)
        brush = QBrush(QtGui.QColor(255, 255, 0, 70))
        qp.setBrush(brush)
        pen = QPen(QtGui.QColor(255, 255, 0, 100))
        qp.setPen(pen)
        qp.drawRect(QRect(self.begin, self.end))

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = event.pos()
        start_point[0] = event.pos().x()
        start_point[1] = event.pos().y()

        print("Start point = ", start_point)
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        self.begin = event.pos()
        self.end = event.pos()
        # Get cursor end position
        end_point[0] = event.pos().x()
        end_point[1] = event.pos().y()

        print("End point = ", end_point)
        self.update()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.savelm_B.setText(_translate("MainWindow", "Save to Landmark"))
        self.saveplot_B.setText(_translate("MainWindow", "Save to Parking Lot"))
        self.back_B.setText(_translate("MainWindow", "BACK"))
        self.next_B.setText(_translate("MainWindow", "NEXT"))
        self.data_stored_label.setText(_translate("MainWindow", "DATA STORED"))
        self.undo_B.setText(_translate("MainWindow", "Undo"))
        self.redo_B.setText(_translate("MainWindow", "Redo"))
        self.reset_B.setText(_translate("MainWindow", "Reset"))
        self.define_parking_lot_label.setText(_translate("MainWindow", "DEFINE PARKING LOT"))
        self.load_B.setText(_translate("MainWindow", "LOAD"))
        # self.image_disp.setText(_translate("MainWindow", "Reference Image"))


class draw_on_qlabel(QWidget):

    def __init__(self, parent=None):
        super(draw_on_qlabel, self).__init__(parent=parent)

        self.draw_canvas = QLabel()
        self.draw_canvas.setGeometry(QtCore.QRect(30, 80, 960, 540))

        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.draw_canvas.setSizePolicy(sizePolicy)
        self.draw_canvas.setMinimumSize(QtCore.QSize(960, 540))
        self.draw_canvas.setMaximumSize(QtCore.QSize(960, 540))

        background = QPixmap(960, 540)
        background.fill(QColor('white'))
        self.draw_canvas.setPixmap(background)
        # self.window_width, self.window_height = 1280, 720
        # self.setFixedSize(self.window_width, self.window_height)

        self.begin = QPoint()
        self.end = QPoint()

    def paintEvent(self, event):
        qp = QPainter(self)
        pixmap = QPixmap(960, 540)
        pixmap.fill(QColor('white'))
        qp.drawPixmap(self.rect(), pixmap)
        brush = QBrush(QtGui.QColor(255, 255, 0, 70))
        qp.setBrush(brush)
        pen = QPen(QtGui.QColor(255, 255, 0, 100))
        qp.setPen(pen)
        qp.drawRect(QRect(self.begin, self.end))

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = event.pos()
        start_point[0] = event.pos().x()
        start_point[1] = event.pos().y()

        print("Start point = ", start_point)
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        self.begin = event.pos()
        self.end = event.pos()
        # Get cursor end position
        end_point[0] = event.pos().x()
        end_point[1] = event.pos().y()

        print("End point = ", end_point)
        self.update()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())