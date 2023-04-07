import menu
import sys
import tenant
import barracuda
from multiprocessing import Process
from multiprocessing import Queue

def load_API(orgs):

    with open("list.txt", "r") as f:
        for line in f:
            if line != []:
                org_data = line.split()
                orgs.append(tenant.Tenant(org_data[0], org_data[1], org_data[2], org_data[3] ))

    return orgs
                
def load_spam(spam_list):
    with open("spam_list.txt", "r") as d:
        for line in d:
            if line != []:
                spam_list.append(line)
            
                
    return spam_list

def main():
    orgs = []
    spam_list= []
    status = False
    queue = Queue()
    processThread = Process(target=barracuda.main, args=(queue,))
    menu.menu(load_API(orgs),load_spam(spam_list), status, processThread,queue)
    

    

if __name__ == "__main__":
    main()
