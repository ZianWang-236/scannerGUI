import time

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
        self.message = "message"
        self.csvfile = None
        self.ctrl = None
        self.csvwriter = None
        self.data = None
        self.watchlist = list()
        self.chgky()
        self.csvname = self.getcsvname()
        self.currpath = self.getcurrpath()
        self.filepath = self.getfilename(self.csvname, self.currpath)
        self.mkdir(self.currpath)
        self.filestat = self.chkfile(self.filepath)

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
            if parcelId not in self.data and parcelId.isalnum() and parcelId not in self.watchlist:
                try:
                    self.csvwriter.writerow([parcelId, datetime.datetime.now().strftime(CSVDATEFORMAT)])
                    self.csvfile.flush()
                    self.data.append(parcelId)
                    self.message = "Next"
                    self.play_sound("/sound/next.mp3")
                except:
                    self.message = "Exception!!!"
                    self.play_sound("/sound/exception.mp3")
            elif parcelId in self.data:
                self.message = "Duplicate"
                self.play_sound("/sound/duplicate.mp3")
            elif not parcelId.isalnum():
                self.message = "Again"
                self.play_sound("/sound/again.mp3")
            elif parcelId in self.watchlist:
                self.message = "Watchlist"
                self.play_sound("/sound/alarm3.wav")

    def closensave(self):
        self.csvfile.flush()
        self.message = "Stop && Save"
        self.play_sound("/sound/stopnsave.mp3")
        self.csvfile.close()


if __name__ == '__main__':
    scannerjob = Scannerjob()
    #todayf = scannerjob.getcsvname()
    currpath = scannerjob.getcurrpath()
    # print(currpath + "/csv")
    #filename = scannerjob.getfilename(todayf, currpath)
    scannerjob.gethistory(0)


