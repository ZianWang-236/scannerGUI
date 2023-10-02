import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import QtTest
from model import *


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.scanner = Scannerjob()
        self.scanner.openfile()
        # self.printstart()
        self.initUi()
    def initUi(self):
        centralwidget = QWidget(self)
        self.setCentralWidget(centralwidget)
        # create main window
        self.setWindowTitle('Scanner')
        self.setMinimumSize(600, 375)
        # self.setMaximumSize(1000, 800)
        self.setGeometry(550, 220, 780, 470)

        # set lable font configuration
        custom_font = QFont()
        custom_font.setFamily("Arial")
        custom_font.setPointSize(16)
        custom_font.setBold(True)

        # create label widget
        self.msg = QLabel('Scanner program:')
        self.msg.setStyleSheet("background-color: #ed2b2a;")
        self.msg.setFont(custom_font)

        # total count label
        self.countlabel = QLabel('Total Count: ')
        #self.countlabel.setStyleSheet("background-color: #ed2b2a;")
        #self.countlabel.setFont(custom_font)

        # create input widget
        self.inputbox = QLineEdit(self)
        self.inputbox.setPlaceholderText("Input Barcode Here")
        self.inputbox.setStyleSheet("background-color: lightblue;")
        self.inputbox.setFont(custom_font)
        self.inputbox.selectAll()

        # create display widget
        self.display = QTextEdit(self)
        self.display.setText("----START!----")
        self.display.setStyleSheet("background-color: #f3d8a2;")
        self.display.setFont(custom_font)
        self.display.setReadOnly(True)

        # container
        self.container = QWidget()
        self.container.setLayout(QVBoxLayout())
        self.container.layout().addWidget(self.display)
        self.container.layout().addWidget(self.inputbox)

        # search input
        self.searchin = QLineEdit(self)
        self.searchin.setPlaceholderText("Search Parcel Id here")
        self.searchin.setStyleSheet("background-color: lightblue;")
        self.searchin.setFont(custom_font)

        # total count display
        self.totalcount = QLabel(self)
        self.totalcount.setFont(custom_font)


        # create control button
        self.startbutton = QPushButton('Start program')
        self.startbutton.setFont(custom_font)
        self.startbutton.setStyleSheet("background-color: #00d084;")
        self.endbutton = QPushButton('Stop and Save')
        self.endbutton.setFont(custom_font)
        self.endbutton.setStyleSheet("background-color: #f44336;")
        self.search = QPushButton('Search')
        self.search.setFont(custom_font)
        self.search.setStyleSheet("background-color: #f5d222;")

        # timer
        self.timer = QTimer(self)

        # connect signal to slots
        self.startbutton.clicked.connect(self.scanner.openfile)
        self.startbutton.clicked.connect(self.printstart)
        self.inputbox.returnPressed.connect(self.display_update)
        self.inputbox.returnPressed.connect(self.totalcount_update)
        self.endbutton.clicked.connect(self.scanner.closensave)
        self.endbutton.clicked.connect(self.printstopnsave)
        self.endbutton.clicked.connect(self.timerstart)
        self.timer.timeout.connect(self.timerstop)

        # configure layout
        layout = QGridLayout(centralwidget)
        layout.setSpacing(20)
        layout.addWidget(self.msg, 0, 3, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.countlabel, 1, 2)
        layout.addWidget(self.totalcount, 1, 3)
        layout.addWidget(self.container, 0, 0, 6, 1)
        layout.addWidget(self.searchin, 2, 3, 1, 2)
        layout.addWidget(self.search, 3, 3, 1, 2)
        layout.addWidget(self.startbutton, 4, 3, 1, 2)
        layout.addWidget(self.endbutton, 5, 3, 1, 2)

        self.setLayout(layout)
        self.show()

    def display_update(self):
        parcelId = self.inputbox.text().strip("\n")
        if parcelId not in self.scanner.data:
            self.display.append(parcelId)
            #print(parcelId)
        self.scanner.writefile(parcelId)
        self.inputbox.clear()

    def printstopnsave(self):
        self.display.append("----STOP AND SAVED!----")
        self.timerstart()

    def timerstart(self, time=20000 ):
        self.timer.start(time)

    def timerstop(self):
        self.timer.stop()
        self.close()

    def printstart(self):
        self.display.append("----START!----")

    def totalcount_update(self):
        count = len(self.scanner.data)
        #print(count)
        self.totalcount.setText(str(count))

    def update_msg(self):
        self.msg.setText(self.scanner.message)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec())

