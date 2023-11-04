from PyQt6.QtGui import *

dlgfont = QFont()
dlgfont.setFamily("Arial")
dlgfont.setPointSize(16)
dlgfont.setBold(True)

# set lable font configuration
uifont = QFont()
uifont.setFamily("Arial")
uifont.setPointSize(16)
uifont.setBold(True)

# font 2
uifontb = QFont()
uifontb.setFamily("Arial")
uifontb.setPointSize(20)
uifontb.setBold(True)

startbtn = """
            QPushButton {
                background-color: #47d147;
                color: Black;
                font-family: Arial;
                font-size: 30px;
                font-weight: bold;
                border: 2px solid #adebad;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #84e184;
                color: Black;
                font-family: Arial;
                font-size: 32px;
                font-weight: bold;
                border: 2px solid #46d246;
                border-radius: 5px;
            }
            QPushButton:disabled {
                background-color: #8c8c8c;
                color: Black;
                font-family: Arial;
                font-size: 30px;
                font-weight: bold;
                border: 2px solid #4d4d4d;
                border-radius: 5px;
            }
            """

stoptbtn = """
            QPushButton {
                background-color: #ff0000;
                color: Black;
                font-family: Arial;
                font-size: 30px;
                font-weight: bold;
                border: 2px solid #ff3333;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #ff4d4d;
                color: Black;
                font-family: Arial;
                font-size: 32px;
                font-weight: bold;
                border: 2px solid #e60000;
                border-radius: 5px;
            }
            QPushButton:disabled {
                background-color: #8c8c8c;
                color: Black;
                font-family: Arial;
                font-size: 30px;
                font-weight: bold;
                border: 2px solid #4d4d4d;
                border-radius: 5px;
            }
            """

cfmtbtn = """
            QPushButton {
                background-color: #f78da7;
                color: Black;
                font-family: Arial;
                font-size: 30px;
                font-weight: bold;
                border: 2px solid #fab7c8;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #f8a0b6;
                color: Black;
                font-family: Arial;
                font-size: 32px;
                font-weight: bold;
                border: 2px solid #f57091;
                border-radius: 5px;
            }
            """