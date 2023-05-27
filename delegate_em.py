from PyQt6 import uic 
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt6 import QtGui
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import tenant
import reset_pw

class Worker(QRunnable):

    def __init__(self, orgs, window, manage,sendas,sendonbehalf,forwarding, fromUser, toUser, remove):
        super(Worker, self).__init__()
        self.orgs = orgs
        self.window = window
        self.manage = manage
        self.sendas = sendas
        self.sendonbehalf = sendonbehalf
        self.forwarding = forwarding
        self.fromUser = fromUser
        self.toUser = toUser
        self.remove = remove


    @pyqtSlot()
    def run(self):
        self.orgs[self.window.clientBox.currentIndex()].delegate_em(self.manage,self.sendas, self.sendonbehalf, self.forwarding, self.fromUser, self.toUser, self.remove)
         


class delegate_em(QWidget):

    def delegate(self, orgs, window,threadpool):
        
        if self.fromUserbox.currentText() == self.toUserbox.currentText():
            print("Cannot delegate to self")
            return 0
        worker = Worker(orgs, window, self.manage.isChecked(), self.sendas.isChecked(),  self.sendonbehalf.isChecked(),  self.forwarding.isChecked(), self.fromUserbox.currentText(), self.toUserbox.currentText(), self.remove.isChecked() )
        threadpool.start(worker)

    def __init__(self, orgs, window, queue, UPNs):
        super().__init__()
        uic.loadUi("email_deleg.ui", self)
        for i in UPNs:
            self.fromUserbox.addItem(i[0])
            self.toUserbox.addItem(i[0])
        
        self.submitBtn2.clicked.connect(lambda: self.delegate(orgs,window,queue))
