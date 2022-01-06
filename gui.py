from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QMessageBox, QFileDialog, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QPixmap, QIcon, QFont, QFontDatabase
from PyQt5 import QtCore
import sys
import base64
import json
import requests


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        # creating our window
        self.setWindowIcon(QIcon('./photos/logo.png'))
        self.setGeometry(150, 70, 600, 900)
        self.setWindowTitle('Tomato Disease Classification')
        self.setAcceptDrops(True)
        self.setStyleSheet("MainWindow {border-image: url('./photos/background.jpg')}")
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.displayDateTime)
        self.timer.start(1000)
        self.initUI()
    
    def initUI(self):
        # creating buttons and labels 
        # to work with QMainWindow, we need to create QWidget and add layouts to QWidget, then set it as central widget for our window

        # layout of our window
        """
        |-------------------------------------------------------|
        | description |   upload button       |                 |
        |-------------------------------------------------------
        |             |   predicted label     |                 |
        |             |   uploaded image      |                 |
        |-------------------------------------------------------
        |             |   predict button      |                 |
        |             |   quit button         |  date and time  |
        |-------------------------------------------------------|
        """
        self.font = QFont("Montserrat-Medium", 14)
        self.description = QLabel("Please upload (or drag and drop) 3D tomato leaf image\nAccepted formats: .png, .jpg, .jpeg, .bmp, .webp")
        self.description.setFont(self.font)

        self.img_description = QLabel("Make sure Image is 3d and 3rd dimension is also 3")
        self.img_description.setFont(self.font)

        self.image_label = QLabel()
        self.image_label.setPixmap(QPixmap('./photos/drop.jpg').scaled(512, 512, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        self.image_label.adjustSize()
        self.image_label.setStyleSheet('background-color: rgb(255, 255, 255);border-radius: 10px;')

        self.predicted_label = QLabel()
        self.predicted_label.setText(f'Result: None\nCondidence score: None')
        self.predicted_label.setFont(QFont("Montserrat-Medium", 16))

        self.datetime = QLabel()
        self.widget = QWidget()

        self.button_size = QtCore.QSize(200, 60)
        self.upload_button = QPushButton('Upload Image')
        self.upload_button.clicked.connect(self.click_upload)
        self.upload_button.setFont(self.font)
        self.upload_button.setFixedSize(self.button_size)
        
        self.predict_button = QPushButton('Predict')
        self.predict_button.clicked.connect(self.click_predict)
        self.predict_button.setFont(self.font)
        self.predict_button.setFixedSize(self.button_size)

        self.quit_button = QPushButton('Quit')
        self.quit_button.clicked.connect(self.click_quit)
        self.quit_button.setFont(self.font)
        self.quit_button.setFixedSize(self.button_size)

        """
        We have 3 main vertical boxes that will be added to horizontal box and it will be set to our widget;
        vbox1 - vertical box for description, position:left
        vbox2 - vertical box that will contain 3 vertical boxes, position:middle
        vbox2_1 - vertical box that will contain push button and be added to vbox2, position:top of vbox2
        vbox2_2 - vertical box that will contain predicted label and uploaded (or dropped) image and be added to vbox2, position:middle of vbox2
        vbox2_3 - vertical box that will contain predict and quit buttons and be added to vbox2, position bottom of vbox2
        vbox3 - vertical box for date and time
        hbox - horizontal box that will contain vbox1, vbox2, and vbox3
        """

        self.vbox1 = QVBoxLayout()
        self.vbox2 = QVBoxLayout()
        self.vbox2_1 = QVBoxLayout()
        self.vbox2_2 = QVBoxLayout()
        self.vbox2_3 = QVBoxLayout()
        self.vbox3 = QVBoxLayout()

        self.vbox1.addWidget(self.description, alignment=QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)

        self.vbox2_1.addWidget(self.img_description, alignment=QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.vbox2_1.addWidget(self.upload_button, alignment=QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        self.vbox2_2.addWidget(self.predicted_label, alignment=QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter)
        self.vbox2_2.addStretch()
        self.vbox2_2.addWidget(self.image_label, alignment=QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        self.vbox2_3.addStretch()
        self.vbox2_3.addWidget(self.predict_button, alignment=QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.vbox2_3.addWidget(self.quit_button, alignment=QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.vbox2_3.addStretch()

        self.vbox2.addStretch()
        self.vbox2.addLayout(self.vbox2_1)
        self.vbox2.addStretch()
        self.vbox2.addLayout(self.vbox2_2)
        self.vbox2.addStretch()
        self.vbox2.addLayout(self.vbox2_3)
        self.vbox2.addStretch()

        self.vbox3.addWidget(self.datetime, alignment=QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)

        self.hbox = QHBoxLayout()
        self.hbox.addLayout(self.vbox1)
        self.hbox.addLayout(self.vbox2)
        self.hbox.addLayout(self.vbox3)
        
        self.widget.setLayout(self.hbox)
        self.setCentralWidget(self.widget)
        self.show()


    # creating live date and time
    def displayDateTime(self):
        self.date = QtCore.QDateTime.currentDateTime()
        displayText = self.date.toString(QtCore.Qt.DefaultLocaleLongDate)
        self.datetime.setText(displayText)
        self.datetime.setFont(self.font)

    # when predict button clicked, image will be sent for prediction to our deployed model
    # and result will be set to predicted_label
    def click_predict(self):
        try:
            with open(self.imagepath, "rb") as f:
                im_bytes = f.read()        

            api = "http://46.101.214.183//predict_request"
            im_b64 = base64.b64encode(im_bytes).decode("utf8")
            headers = {"Content-type": "application/json", "Accept": "text/plain", "key":"59367"}
    
            payload = json.dumps({"image": im_b64})
            response = requests.post(api, data=payload, headers=headers)
        
            if "wrong dim" in response.json():
                self.predicted_label.setText(response.json()["wrong dim"])
                    
            else:
                data = response.json()
                label = data['label']    
                score = data['confidence score']
                self.predicted_label.setText(f'Result: {label}\nCondidence score: {score}')
            self.predicted_label.adjustSize()        

        except:
            pass

    # showing message box for confirmation of closing the app when close - x clicked
    def closeEvent(self, event):
        close_reply=QMessageBox.question(self,'Message','Are you sure you want to quit?',\
                                         QMessageBox.Yes|QMessageBox.No,QMessageBox.No )
        if close_reply==QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
    
    # showing message box for confirmation of closing the app when quit button clicked
    def click_quit(self):
        quit_reply=QMessageBox.question(self,'Message','Are you sure you want to quit?',\
                                        QMessageBox.Yes|QMessageBox.No,QMessageBox.No )
        if quit_reply==QMessageBox.Yes:
            QApplication.instance().quit()
        else:
            pass

    # when uplad button clicked, we read the image path and show the image on the window
    def click_upload(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File', '.', "Image file(*.jpg *.jpeg *.png *.bmp *.webp)")
        self.imagepath = filename[0]
        if self.imagepath == '':
            self.predicted_label.setText(f'Result: Image not uploaded\nCondidence score: None')
            self.image_label.setPixmap(QPixmap('./photos/drop.jpg').scaled(512, 512, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        
        else:
            self.image_label.setPixmap(QPixmap(self.imagepath).scaled(512, 512, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
            
    # accepting drag event if it has image object and file format is in correct form
    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:
            file_name = event.mimeData().text()
            if file_name.split('.')[-1] in ['png', 'jpg', 'jpeg', 'bmp', 'webp']:
                event.accept()
        else:
            event.ignore()

    # same for the dragMove
    def dragMoveEvent(self, event):
        if event.mimeData().hasImage:
            file_name = event.mimeData().text()
            if file_name.split('.')[-1] in ['png', 'jpg', 'jpeg', 'bmp', 'webp']:
                event.accept()
        else:
            event.ignore()

    # when proper image file is dropped read file path, and show the image on the window 
    def dropEvent(self, event):
        if event.mimeData().hasImage:
            file_name = event.mimeData().text()
            if file_name.split('.')[-1] in ['png', 'jpg', 'jpeg', 'bmp', 'webp']:
                event.setDropAction(QtCore.Qt.CopyAction)
                file_path = event.mimeData().urls()[0].toLocalFile()
                self.image_label.setPixmap(QPixmap(file_path).scaled(512, 512, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))

            event.accept()
        else:
            event.ignore()

       
def main():
    app = QApplication(sys.argv)    
    QFontDatabase.addApplicationFont("fonts/Montserrat-Medium.ttf")
    win = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()