import sys
import mainwindow
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt6 import QtGui
import tenant

#Load List of tenants and related APIs from list.txt
def load_API(orgs):
        with open("list.txt") as f:
            for line in f:
                if line != []:
                    org_data = line.split()
                    orgs.append(tenant.Tenant(org_data[0], org_data[1], org_data[2], org_data[3], org_data[4], org_data[5]))                  
        return orgs

#load list of Barracuda Email Security clients
def load_cls(bar_list):
        with open("spam_list.txt", "r") as d:
            for line in d:
                if line != []:
                    bar_list.append(line)
        return bar_list

#initializes tenants and bar_list, then passes them to mainwindow
def main():
    orgs = []
    bar_list = []

    orgs = load_API(orgs)
    bar_list = load_cls(bar_list)


    mainwindow.inito(orgs, bar_list)



#initializer 
if __name__ == "__main__":
    main()
