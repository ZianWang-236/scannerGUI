import sys
import subprocess
import pyperclip

#import PyQt6.QtWidgets.QMainWindow
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from model import *
from style import *
from const import *


class generaicDialog(QDialog):
    def __init__(self, winttl, msg, btnmsg: str):
        super().__init__()
        self.setWindowTitle(winttl)
        self.layout = QVBoxLayout()

        self.message = QLabel(msg)
        self.message.setFont(dlgfont)

        self.btn = QPushButton(btnmsg)
        self.btn.setFont(dlgfont)
        self.btn.clicked.connect(self.done)

        self.layout.addWidget(self.message)
        self.layout.addWidget(self.btn)
        self.setLayout(self.layout)

class watchlistDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Set Successful!")
        self.layout = QVBoxLayout()

        self.message = QLabel("watchlist set successful")
        self.message.setFont(dlgfont)

        self.btn = QPushButton("OK")
        self.btn.setFont(dlgfont)
        self.btn.clicked.connect(self.done)

        self.layout.addWidget(self.message)
        self.layout.addWidget(self.btn)
        self.setLayout(self.layout)

class copyDiaglog(QDialog):
    def __init__(self, scanner:Scannerjob):
        super().__init__()
        self.setWindowTitle("Copy Successful!")
        self.layout = QVBoxLayout()

        self.message = QLabel("Copied " + str(len(scanner.data)) + " ID")
        self.message.setFont(dlgfont)

        self.btn = QPushButton("OK")
        self.btn.setFont(dlgfont)
        self.btn.clicked.connect(self.done)

        self.layout.addWidget(self.message)
        self.layout.addWidget(self.btn)
        self.setLayout(self.layout)

class confirmDiaglog(QDialog):
    def __init__(self, scanner:Scannerjob):
        super().__init__()
        self.setWindowTitle("Delete Successful!")
        self.layout = QVBoxLayout()

        self.message = QLabel("Deleted Successful!")
        self.message.setFont(dlgfont)

        self.btn = QPushButton("OK")
        self.btn.setFont(dlgfont)
        self.btn.clicked.connect(self.done)

        self.layout.addWidget(self.message)
        self.layout.addWidget(self.btn)
        self.setLayout(self.layout)

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.scanner = Scannerjob()
        self.scanner.openfile()
        self.initUi()
        self.update_msg()
    def initUi(self):
        centralwidget = QWidget(self)
        self.setCentralWidget(centralwidget)
        # create main window
        self.setWindowTitle('Scanner V3.0')
        self.setMinimumSize(1035, 643)
        # self.setMaximumSize(1000, 800)
        # self.setGeometry(550, 220, 1035, 643)



        # menu
        bar = self.menuBar()
        menu_file = bar.addMenu('Files')

        cpyall_action = QAction("Copy all Parcel Id", self)
        cpyall_action.triggered.connect(self.cpyall)

        opencsv_action = QAction("Open csv location", self)
        opencsv_action.triggered.connect(self.opencsvloc)

        opendir_action = QAction("Open program location", self)
        opendir_action.triggered.connect(self.openprogloc)

        menu_setting = bar.addMenu('Settings')
        chkbox_action = QWidgetAction(self)
        chkbox_widget =QCheckBox('auto open CSV when stopped', self)
        chkbox_widget.stateChanged.connect(self.chgCSVset)
        chkbox_action.setDefaultWidget(chkbox_widget)

        # menu_data = bar.addMenu('Data')
        # del_id = QAction("delete specific ID", self)
        # del_id.triggered.connect(self.delid)

        menu_setting.addAction(chkbox_action)


        menu_file.addAction(opencsv_action)
        menu_file.addAction(opendir_action)
        menu_file.addAction(cpyall_action)

        # menu_data.addAction(del_id)

        # -----------------------------------------LEFT widgets------------------------------------------
        # create input widget
        self.inputbox = QLineEdit(self)
        self.inputbox.setPlaceholderText("Input Barcode Here")
        self.inputbox.setStyleSheet("background-color: #B3E5FC;")
        self.inputbox.setFont(uifont)

        # create display widget
        self.display = QTextEdit(self)
        self.display.setText("---------------START!---------------")
        self.display.setStyleSheet("background-color: #f3d8a2;")
        self.display.setFont(uifont)
        self.display.setReadOnly(True)

        # -----------------------------------------RIGHT widgets------------------------------------------
        # msg label
        self.msglabel = QLabel('Scanner program:')
        # self.msglabel.setStyleSheet("background-color: #ed2b2a;")
        self.msglabel.setFont(uifont)

        self.msgbox = QLabel()
        self.msgbox.setText("Messages")
        self.msgbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.msgbox.setFont(uifontb)

        # total count label
        self.countlabel = QLabel('Total Count: ')
        self.countlabel.setFont(uifont)

        # total count display
        self.totalcount = QLabel("0")
        self.totalcount.setFont(uifontb)
        self.totalcount.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # search input
        self.searchin = QLineEdit(self)
        self.searchin.setPlaceholderText("Search Parcel ID here")
        self.searchin.setStyleSheet("background-color: #B3E5FC;")
        self.searchin.setFont(uifont)

        # create control button
        self.startbutton = QPushButton('Start')
        self.startbutton.setStyleSheet(startbtn)
        if self.scanner.stat:
            self.startbutton.setEnabled(False)
        else:
            self.startbutton.setEnabled(True)

        self.stopbutton = QPushButton('Stop && Save')
        self.stopbutton.setStyleSheet(stoptbtn)
        if self.scanner.stat:
            self.stopbutton.setEnabled(True)
        else:
            self.stopbutton.setEnabled(False)

        self.search = QPushButton('Search')
        self.search.setStyleSheet("background-color: #f5d222;")

        # watch list input
        self.watchlist = QTextEdit()
        self.watchlist.setPlaceholderText('Input watch list, seperate with ENTER')
        self.watchlist.setFont(uifont)
        self.watchlist.setStyleSheet("background-color: #B3E5FC;")
        self.watchlist.setCursorWidth(5)

        # watchlist button
        self.watchlistbutton = QPushButton('Confirm Watchlist')
        self.watchlistbutton.setStyleSheet(cfmtbtn)
        self.watchlistbutton.setFont(uifont)

        # delid input
        self.delidInput = QLineEdit(self)
        self.delidInput.setPlaceholderText("DELETE Parcel ID")
        self.delidInput.setStyleSheet("background-color: #B3E5FC;")
        self.delidInput.setFont(uifont)

        self.delidbutton = QPushButton('DELETE')
        self.delidbutton.setStyleSheet(delidbtn)
        self.delidbutton.setFont(uifont)

        # -----------------------------------------containers------------------------------------------
        # msg container
        self.containermsglb = QWidget()
        self.containermsglb.setLayout(QHBoxLayout())
        self.containermsglb.setStyleSheet("border: 2px solid black")
        self.containermsglb.layout().addWidget(self.msglabel)
        self.containermsglb.layout().addWidget(self.msgbox)

        # total count container
        self.containerttc = QWidget()
        self.containerttc.setLayout(QHBoxLayout())
        self.containerttc.setStyleSheet("border: 2px solid black")
        self.containerttc.layout().addWidget(self.countlabel)
        self.containerttc.layout().addWidget(self.totalcount)

        # watchlist container
        self.watchlistcontainer = QWidget()
        self.watchlistcontainer.setLayout(QVBoxLayout())
        self.watchlistcontainer.setStyleSheet("border: 2px solid black")
        self.watchlistcontainer.layout().addWidget(self.watchlist)
        self.watchlistcontainer.layout().addWidget(self.watchlistbutton)

        # button container search etc
        self.containerbtn_srh = QWidget()
        self.containerbtn_srh.setLayout(QVBoxLayout())
        self.containerbtn_srh.setStyleSheet("border: 2px solid black")
        self.containerbtn_srh.layout().addWidget(self.searchin)
        self.containerbtn_srh.layout().addWidget(self.search)

        # delid container
        self.delidcontainer = QWidget()
        self.delidcontainer.setLayout(QVBoxLayout())
        self.delidcontainer.setStyleSheet("border: 2px solid black")
        self.delidcontainer.layout().addWidget(self.delidInput)
        self.delidcontainer.layout().addWidget(self.delidbutton)


        # button container start and stop
        self.containerbtn_sns = QWidget()
        self.containerbtn_sns.setLayout(QHBoxLayout())
        self.containerbtn_sns.setStyleSheet("border: 2px solid black")
        self.containerbtn_sns.layout().addWidget(self.startbutton)
        self.containerbtn_sns.layout().addWidget(self.stopbutton)

        # -----------------------------------------LEFT------------------------------------------
        self.containerl = QWidget()
        self.containerl.setLayout(QVBoxLayout())
        self.containerl.setStyleSheet("border: 2px solid black")
        self.containerl.layout().addWidget(self.display)
        self.containerl.layout().addWidget(self.inputbox)

        # -----------------------------------------RIGHT------------------------------------------
        self.containerr = QWidget()
        self.containerr.setLayout(QVBoxLayout())
        self.containerr.setStyleSheet("border: 2px solid black")
        self.containerr.layout().addWidget(self.containermsglb)
        self.containerr.layout().addWidget(self.containerttc)
        # self.containerr.layout().addWidget(self.containerbtn_srh)
        self.containerr.layout().addWidget(self.watchlistcontainer)
        self.containerr.layout().addWidget(self.delidcontainer)
        self.containerr.layout().addWidget(self.containerbtn_sns)

        # timer
        self.timer = QTimer(self)
        # -----------------------------------------connect signal to slots------------------------------------------
        self.startbutton.clicked.connect(self.scanner.openfile)
        self.startbutton.clicked.connect(self.update_msg)
        self.startbutton.clicked.connect(self.printstart)
        self.startbutton.clicked.connect(self.refreshbtn)
        self.inputbox.returnPressed.connect(self.display_update)
        self.inputbox.returnPressed.connect(self.totalcount_update)
        self.inputbox.returnPressed.connect(self.update_msg)
        self.stopbutton.clicked.connect(self.scanner.closensave)
        self.stopbutton.clicked.connect(self.update_msg)
        self.stopbutton.clicked.connect(self.printstopnsave)
        self.stopbutton.clicked.connect(self.refreshbtn)
        self.watchlistbutton.clicked.connect(self.readwatchlist)
        self.delidbutton.clicked.connect(self.delid)
        # -----------------------------------------configure layout------------------------------------------
        layout = QHBoxLayout(centralwidget)
        layout.setSpacing(20)
        layout.addWidget(self.containerl)
        layout.addWidget(self.containerr)

        self.setLayout(layout)
        self.show()

    # -----------------------------------------slots------------------------------------------
    def readwatchlist(self):
        watchlist = self.watchlist.toPlainText().split('\n')
        watchlist = list(watchlist)
        # dlg = watchlistDialog()
        # dlg.exec()
        if watchlist[-1] == '':
            watchlist.pop()
        self.scanner.watchlist = watchlist
        dlg = generaicDialog("Complete!", "Set Complete!\n " + str(len(self.scanner.watchlist)) + " Parcel ID added!", "OK")
        dlg.exec()
        if DEBUG:
            print(self.scanner.watchlist)

    def opencsvloc(self):
        subprocess.Popen(['explorer', r"" + os.path.dirname(os.path.realpath(__file__)) + "\csv"])

    def openprogloc(self):
        subprocess.Popen(['explorer', r"" + os.path.dirname(os.path.realpath(__file__))])

    def display_update(self):
        parcelId = self.inputbox.text().strip("\n")
        if parcelId not in self.scanner.data:
            # if parcelId.isnumeric() and len(parcelId) == SDLEN:
            #     parcelId = "\'" + parcelId
            self.display.append(parcelId)
        self.scanner.writefile(parcelId)
        self.inputbox.clear()

    def printstopnsave(self):
        self.display.append("---------------STOP AND SAVED!---------------")


    def printstart(self):
        self.display.append("---------------START!---------------")

    def totalcount_update(self):
        count = len(self.scanner.data)
        #print(count)
        self.totalcount.setText(str(count))

    def update_msg(self):
        if DEBUG:
            print(self.scanner.message)
        self.msgbox.setText(self.scanner.message)

    def cpyall(self):
        pyperclip.copy("\n".join(self.scanner.data))
        dlg = copyDiaglog(self.scanner)
        dlg.exec()

    def delid(self):
        print("button clicked")
        delid = self.delidInput.text().strip("\n")
        print("id got: " + delid)
        print("scanner data: " + str(self.scanner.data))
        res = False
        if delid in self.scanner.data:
            res = self.scanner.delid(delid)
        if res == True:
            dlg = generaicDialog("Delete success!", "Delete success!","OK")
            dlg.exec()
        else:
            dlg = generaicDialog("Delete Fail!", "Id not in system", "OK")
            dlg.exec()





    def refreshbtn(self):
        if self.scanner.stat:
            self.startbutton.setEnabled(False)
            self.stopbutton.setEnabled(True)
            self.inputbox.setEnabled(True)
        else:
            self.startbutton.setEnabled(True)
            self.inputbox.setEnabled(False)
            self.stopbutton.setEnabled(False)

    def chgCSVset(self):
        self.scanner.autoopencsv = False if self.scanner.autoopencsv else True




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec())

