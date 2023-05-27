from PyQt6 import uic 
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt6 import QtGui

#class to reset password
class reset_pw(QWidget):
       
    def reset(self, value, orgs, window):

        if (self.password_1.text() != self.password_2.text()) or (len(self.password_1.text()) < 6):
            print("Check the password")
        else:
            orgs[window.clientBox.currentIndex()].reset_pw(value, self.checkForce.isChecked(), window, self.password_1.text())

    
    def __init__(self, value, orgs, window):
        super().__init__()
        uic.loadUi("reset_pw.ui", self)
        self.usern_label.setText(value)
        self.submitBtn.clicked.connect(lambda: self.reset(value,orgs,window))