# Import packages
import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QLabel

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
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# Define new class for Define Parking Lot window
class define_parking_lot(object):

    def setupUi(self, MainWindow):

        # Create MainWindow instance
        MainWindow.setObjectName("MainWindow")

        MainWindow.setMinimumSize(QtCore.QSize(1280, 720))
        MainWindow.setMaximumSize(QtCore.QSize(1280, 720))
        MainWindow.setStyleSheet(lightgray_stylesheet)

        # Create a central widget object, used as a reference to other objects
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Define label fonts
        label_font = QtGui.QFont()
        label_font.setFamily("Montserrat")
        label_font.setPointSize(16)
        label_font.setBold(True)
        label_font.setItalic(False)
        label_font.setWeight(75)

        # Define window label
        self.define_parking_lot_label = QtWidgets.QLabel(self.centralwidget)
        self.define_parking_lot_label.setGeometry(QtCore.QRect(460, 20, 410, 40))
        self.define_parking_lot_label.setFont(label_font)
        self.define_parking_lot_label.setStyleSheet(teal_label_stylesheet)
        self.define_parking_lot_label.setText("DEFINE PARKING LOT")
        self.define_parking_lot_label.setAlignment(QtCore.Qt.AlignCenter)
        self.define_parking_lot_label.setObjectName("define_parking_lot_label")

        # Stored ata box label
        self.data_stored_label = QtWidgets.QLabel(self.centralwidget)
        self.data_stored_label.setGeometry(QtCore.QRect(1020, 40, 230, 30))
        self.data_stored_label.setFont(label_font)
        self.data_stored_label.setStyleSheet("color: rgb(75, 75, 75);")
        self.data_stored_label.setText("DATA STORED")
        self.data_stored_label.setAlignment(QtCore.Qt.AlignCenter)
        self.data_stored_label.setObjectName("data_stored_label")

        # Stored data box (Text box)
        self.data_list = QtWidgets.QListWidget(self.centralwidget)
        self.data_list.setGeometry(QtCore.QRect(1020, 80, 230, 270))
        self.data_list.setMaximumSize(QtCore.QSize(240, 270))
        self.data_list.setStyleSheet(darkgray_stylesheet)
        self.data_list.setObjectName("data_list")

        # Define button fonts
        button_font = QtGui.QFont()
        button_font.setFamily("Montserrat")
        button_font.setPointSize(12)
        button_font.setBold(True)
        button_font.setItalic(False)
        button_font.setWeight(75)

        # Define button layouts
        # First: horizontal layout, for bottom left buttons
        self.horz_layout_widget = QtWidgets.QWidget(self.centralwidget)
        self.horz_layout_widget.setGeometry(QtCore.QRect(20, 630, 430, 80))
        self.horz_layout_widget.setObjectName("horz_layout_widget")
        # Add horizontal layout widget
        self.horz_layout_1 = QtWidgets.QHBoxLayout(self.horz_layout_widget)
        self.horz_layout_1.setContentsMargins(0, 0, 0, 0)
        self.horz_layout_1.setObjectName("horz_layout_1")
        # Add buttons
        # Save to landmark button
        self.save_landmark_B = QtWidgets.QPushButton(self.horz_layout_widget)
        self.save_landmark_B.setMaximumSize(QtCore.QSize(270, 40))
        self.save_landmark_B.setFont(button_font)
        self.save_landmark_B.setStyleSheet(yellow_button_stylesheet)
        self.save_landmark_B.setText("Save to Landmark")
        self.save_landmark_B.setObjectName("save_landmark_B")
        self.horz_layout_1.addWidget(self.save_landmark_B)
        # Save to parking slot button
        self.save_parklot_B = QtWidgets.QPushButton(self.horz_layout_widget)
        self.save_parklot_B.setMaximumSize(QtCore.QSize(270, 40))
        self.save_parklot_B.setFont(button_font)
        self.save_parklot_B.setStyleSheet(teal_button_stylesheet)
        self.save_parklot_B.setText("Save to Parking Slot")
        self.save_parklot_B.setObjectName("save_parklot_B")
        self.horz_layout_1.addWidget(self.save_parklot_B)


        # Second: horizontal layout, for bottom right buttons
        self.horz_layout_widget_2 = QtWidgets.QWidget(self.centralwidget)
        self.horz_layout_widget_2.setGeometry(QtCore.QRect(1010, 630, 261, 80))
        self.horz_layout_widget_2.setObjectName("horz_layout_widget_2")
        # Add horizontal layout widget
        self.horz_layout_2 = QtWidgets.QHBoxLayout(self.horz_layout_widget_2)
        self.horz_layout_2.setContentsMargins(0, 0, 0, 0)
        self.horz_layout_2.setObjectName("horz_layout_2")
        # Add buttons
        # Back button
        self.back_B = QtWidgets.QPushButton(self.horz_layout_widget_2)
        self.back_B.setMaximumSize(QtCore.QSize(100, 40))
        self.back_B.setFont(button_font)
        self.back_B.setStyleSheet(gray_button_stylesheet)
        self.back_B.setText("BACK")
        self.back_B.setObjectName("back_B")
        self.horz_layout_2.addWidget(self.back_B)
        # Next button
        self.next_B = QtWidgets.QPushButton(self.horz_layout_widget_2)
        self.next_B.setMaximumSize(QtCore.QSize(100, 40))
        self.next_B.setFont(button_font)
        self.next_B.setStyleSheet(teal_button_stylesheet)
        self.next_B.setText("NEXT")
        self.next_B.setObjectName("next_B")
        self.horz_layout_2.addWidget(self.next_B)
        
        # Third: vertical layout, for defining navigation buttons
        self.vert_layout_widget = QtWidgets.QWidget(self.centralwidget)
        self.vert_layout_widget.setGeometry(QtCore.QRect(1020, 360, 100, 170))
        self.vert_layout_widget.setObjectName("vert_layout_widget")
        
        self.vert_layout_1 = QtWidgets.QVBoxLayout(self.vert_layout_widget)
        self.vert_layout_1.setContentsMargins(0, 0, 0, 0)
        self.vert_layout_1.setObjectName("vert_layout_1")

        # Undo button
        self.undo_B = QtWidgets.QPushButton(self.vert_layout_widget)
        self.undo_B.setMaximumSize(QtCore.QSize(100, 40))
        self.undo_B.setFont(button_font)
        self.undo_B.setStyleSheet(gray_button_stylesheet)
        self.undo_B.setText("Undo")
        self.undo_B.setObjectName("undo_B")
        self.vert_layout_1.addWidget(self.undo_B)
        # Redo button
        self.redo_B = QtWidgets.QPushButton(self.vert_layout_widget)
        self.redo_B.setMaximumSize(QtCore.QSize(100, 40))
        self.redo_B.setFont(button_font)
        self.redo_B.setStyleSheet(teal_button_stylesheet)
        self.redo_B.setText("Redo")
        self.redo_B.setObjectName("redo_B")
        self.vert_layout_1.addWidget(self.redo_B)
        # Reset
        self.reset_B = QtWidgets.QPushButton(self.vert_layout_widget)
        self.reset_B.setMaximumSize(QtCore.QSize(100, 40))
        self.reset_B.setFont(button_font)
        self.reset_B.setStyleSheet(red_button_stylesheet)
        self.reset_B.setText("Reset")
        self.reset_B.setObjectName("reset_B")
        self.vert_layout_1.addWidget(self.reset_B)

        # Image viewer
        self.image_viewer = QtWidgets.QLabel(self.centralwidget)
        self.image_viewer.setGeometry(QtCore.QRect(30, 80, 960, 540))
        self.image_viewer.setMaximumSize(QtCore.QSize(960, 540))
        self.image_display = image_editor(self.image_viewer)
        self.display_image()

        # Add mouse event position variables
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()

        MainWindow.setCentralWidget(self.centralwidget)

    def display_image(self):
        background = QtGui.QPixmap(filename)
        scaled_background = background.scaled(960, 540)
        self.image_viewer.setPixmap(scaled_background)

def image_editor(QLabel):
    x0 = 0
    y0 = 0
    x1 = 0
    y1 = 0
    flag = False
    # Set up image editor
    def mousePressEvent(self, event):
        # Initiate passing_object to this new object
        self.flag = True
        self.x0 = event.x()
        self.y0 = event.y()

    def mouseReleaseEvent(self, event):
        self.flag = False

    def mouseMoveEvent(self, event):
        if self.flag:
            self.x1 = event.x()
            self.y1 = event.y()
            self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        rectangle = QtCore.QRect(self.x0, self.y0, abs(self.x1 - self.x0) , abs(self.y1 - self.y0))
        painter = QtGui.QPainter(self)
        painter.setPen(QtGui.QPen(QtCore.Qt.red, 2, QtCore.Qt.SolidLine))
        painter.drawRect(rectangle)
# ----------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = define_parking_lot()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())