from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from main_ver2 import main
from input_class import *

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()
    #############   

    def setupUI(self):
        self.setGeometry(300, 200, 500, 300)
        self.setWindowTitle("  v2.0")
        self.setWindowIcon(QIcon('icon.png'))

        self.pushButton = QPushButton('file open')
        self.pushButton.clicked.connect(self.pushButtonClicked)

        self.label = QLabel()




        self.lineEdit_username = QLineEdit()
        self.lineEdit_username.setPlaceholderText('username')
        self.lineEdit_password = QLineEdit()
        self.lineEdit_password.setPlaceholderText('password')

        self.lineEdit = QLineEdit()
        self.lineEdit.setPlaceholderText('commend')

        self.pushButton0 = QPushButton("run")
        self.pushButton0.clicked.connect(self.init_main)


        # Right Layout
        rightLayout = QVBoxLayout()
        rightLayout.addWidget(self.pushButton)
        rightLayout.addWidget(self.label)
        rightLayout.addWidget(self.lineEdit_username)
        rightLayout.addWidget(self.lineEdit_password)
        rightLayout.addWidget(self.lineEdit)
        rightLayout.addWidget(self.pushButton0)

        rightLayout.addStretch(1)

        layout = QHBoxLayout()

        layout.addLayout(rightLayout)

        layout.setStretchFactor(rightLayout, 0)

        self.setLayout(layout)
    #############   

    def init_main(self):
        print(self.lineEdit_username.text())
        print(self.lineEdit_password.text())
        print(self.lineEdit.text())
    
        main()

    def pushButtonClicked(self):
        fname = QFileDialog.getOpenFileName(self)
        self.label.setText(fname[0])

        userdata = Userdata()

        userdata.set_filepath(fname[0])
        print('--------------')
        print(userdata.get_filepath())
        print('--------------')


 