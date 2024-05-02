import time
import subprocess
import csv
import datetime
import os
import playsound
from win32con import WM_INPUTLANGCHANGEREQUEST
import win32gui
import win32api


from const import *


class Scannerjob:
    def __init__(self):
        self.autoopencsv = False
        self.stat = True
        self.message = "message"
        self.msgrtn = -1
        self.csvfile = None
        self.ctrl = None
        self.csvwriter = None
        self.data = list()
        self.watchlist = list()
        self.csvname = self.getcsvname()
        self.currpath = self.getcurrpath()
        self.filepath = self.getfilename(self.csvname, self.currpath)
        self.mkdir(self.currpath)
        self.filestat = self.chkfile(self.filepath)
        self.chgky()
        self.delflag = False

    @staticmethod
    def slashformat(before: str) -> str:
        return before.replace("\\", "/")

    def chgky(self) -> int:
        # get window
        hwnd = win32gui.GetForegroundWindow()
        # get keyboard layout
        im_list = win32api.GetKeyboardLayoutList()
        im_list = list(map(hex, im_list))
        exist = set(im_list) and set(KEYLAYOUT)
        if exist != None:
            # set to English
            result = win32api.SendMessage(
                hwnd,
                WM_INPUTLANGCHANGEREQUEST,
                0,
                exist.pop())
            if DEBUG:
                print("change keyboard result: " + str(result))
            return 0 # switch successful
        else:
            self.play_sound("/sound/alarm3.wav ")
            return -1 # no workable language layout

    def gethistory(self, opt:int = 0):
        # print(self.currpath)
        ls = []
        for filename in os.listdir(self.currpath + "/csv"):
            f = os.path.join(self.currpath + "/csv/", filename)
            if os.path.isfile(f):
                ls.append(time.strptime(filename.strip('.csv'), '%Y-%m-%d'))
                print(time.strptime(filename.strip('.csv'), '%Y-%m-%d'))
        print(((time.mktime(ls[-1]) - time.mktime(ls[0]))//(3600*24)))

    # check if buffered time and current time are the same, if not pop up for restart
    def chkTdiff(self):
        pass

    def delid(self, id:str) -> bool:
        print("func activate")
        print("self.data: " + str(self.data))
        if id.strip("\n") in self.data:
            self.data.remove(id.strip("\n"))
            self.play_sound("/sound/success.wav ")
            return True
        else:
            # self.play_sound("/sound/fail.wav ")
            return False

    # datetime
    def getcsvname(self) -> str:
        csvname = datetime.datetime.now()
        csvname = csvname.strftime(CSVNAMEFORMAT)
        return csvname

    # get current path
    def getcurrpath(self) -> str:
        currpath = os.path.dirname(os.path.realpath(__file__))
        currpath = self.slashformat(currpath)
        return currpath

    # generate file name
    def getfilename(self, csvname, currpath: str) -> str:
        filename = csvname + ".csv"
        filepath = os.path.join(currpath + "/csv", filename)
        filepath = self.slashformat(filepath)
        return filepath

    def mkdir(self, currpath):
        # check if file path exists, if not, create csv path
        if not os.path.exists(currpath + "/csv"):
            os.mkdir(currpath + "/csv")

    def chkfile(self, filepath):
        res = os.path.exists(filepath)
        return res

    def getctrl(self, ifexists):
        return 'a' if ifexists else 'w'

    def getfields(self, ctrl):
        return WFIELDS if ctrl == 'w' else AFIELDS

    # play sound file from given folder
    def play_sound(self, filename: str):
        playsound.playsound(self.currpath + filename)

    def openfile(self):
        self.data = []
        self.filestat = self.chkfile(self.filepath)
        self.ctrl = self.getctrl(self.filestat)
        self.csvfile = open(self.filepath, self.ctrl, newline='')
        self.csvwriter = csv.writer(self.csvfile)
        self.message = "Start"
        self.stat = True
        # self.csvwriter.writerow(self.getfields(self.filestat))
        self.play_sound("/sound/start.mp3")
        # return csvfile

    # def gethistory(self):
    #     try:
    #         with open(self.filepath, 'r', newline='') as f:
    #             reader = csv.reader(f)
    #             for row in reader:
    #                 self.data.append(row[0])
    #             print(self.data)
    #     except:
    #         self.message = "get history failied!"

    def getcsvwriter(self):
        return csv.writer(self.csvfile)

    def writefile(self, parcelId: str):
        if len(parcelId) < 5:
            self.play_sound("/sound/again.mp3")
        else:
            if parcelId not in self.data and parcelId not in self.watchlist and parcelId.isalnum():
                try:
                    if parcelId.isnumeric() and len(parcelId) == SDLEN:
                        self.csvwriter.writerow(['\'' + parcelId, datetime.datetime.now().strftime(CSVDATEFORMAT)])
                        self.data.append('\'' + parcelId)
                        self.message = "Next"
                        self.play_sound("/sound/next.mp3")
                    elif parcelId.isnumeric() and len(parcelId) < SDLEN:
                        self.message = "Again"
                        self.play_sound("/sound/again.mp3")
                    elif parcelId.isalnum():
                        self.csvwriter.writerow([parcelId.upper(), datetime.datetime.now().strftime(CSVDATEFORMAT)])
                        self.data.append(parcelId)
                        self.message = "Next"
                        self.play_sound("/sound/next.mp3")
                    self.csvfile.flush()
                    # self.message = "Next"
                    # self.play_sound("/sound/next.mp3")
                except:
                    self.message = "Exception!!!"
                    self.play_sound("/sound/exception.mp3")
            # elif parcelId.isnumeric() and len(parcelId) >= 16:

            elif parcelId in self.data:
                self.message = "Duplicate"
                self.play_sound("/sound/next.mp3")
            elif not parcelId.isalnum():
                self.message = "Again"
                self.play_sound("/sound/again.mp3")
            elif parcelId in self.watchlist:
                self.message = "Watchlist"
                self.play_sound("/sound/alarm3.wav")

    def closensave(self):
        self.csvfile.flush()
        self.message = "Stop && Save"
        self.stat = False
        self.play_sound("/sound/stopnsave.mp3")
        self.csvfile.close()
        if self.autoopencsv:
            subprocess.Popen(['explorer', r"" + os.path.dirname(os.path.realpath(__file__)) + "\csv"])



if __name__ == '__main__':
    scannerjob = Scannerjob()
    #todayf = scannerjob.getcsvname()
    currpath = scannerjob.getcurrpath()
    # print(currpath + "/csv")
    #filename = scannerjob.getfilename(todayf, currpath)
    scannerjob.gethistory(0)


