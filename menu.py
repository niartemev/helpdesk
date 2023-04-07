import sys
import threading, os
from subprocess import call
from multiprocessing import Process
from multiprocessing import Queue
import barracuda
import time

def select(orgs, org_index, spam_list, spam_cl):

    choice = input("client: ")
    count = 0
    track = 0

    if choice == "0":
        sys.exit()

    for org in orgs:
        track += 1
        if choice.lower() in org.name.lower():
            count +=1
            org_index = track
            
    count_sp = 0
    track_sp = 0
    spam_cl = " "
    
    for item in spam_list:
        track_sp += 1
        if choice.lower() in item.lower():
            count_sp += 1
            spam_cl = item
    

    
    if count > 1 :
        print("More than 1 match found,try again")
        return 1,spam_cl
    
    elif (count == 0 and count_sp == 1):
        print("API NO, BARRACUDA YES???")
        choice_2 = int(input("1 - Yes, 0 - No:"))
        if choice_2 == 1:
            return 2,spam_cl
        elif choice_2 == 0:
            return 1,spam_cl
    elif count == 1:
        return 0,org_index-1

    elif count != 1:
        print("No matches found")
        return 1,spam_cl




def user_ops(orgs,org_index):
    
    while True:
        result = orgs[org_index].select_user()
        if result == 1:
            print("failed to select")
        elif result == 2:
            break
        else:
            while True:
                print("1 - password reset, 2 - mailbox delegation, 3 - update user info, 4 - go back")
                choice = input(": ")
                if choice == "1" :
                    orgs[org_index].reset_pw()
                elif choice == "2" :
                    orgs[org_index].delegation()
                elif choice == "3" :
                    orgs[org_index].update_usr()
                elif choice == "4":
                    break
                else:
                    print("Wrong option, try again")
            
        


def sub_menu(orgs,org_index):

    while True:
        print("(1 - user. 2 - spam. 3 - go back)")

        option = int(input(": "))
        if option == 1:
            user_ops(orgs,org_index)
        elif option == 2:
            orgs[org_index].spam_block()
        elif option == 3:
            break


def sub_block_spm(customer,status,queue,processThread):
    print("Spam OP for " + customer + " 1 - block, 2 - whitelist, 3 - back")
    action = input(":")
    if int(action) == 3:
        return 0
    elif (int(action) != 2 and int(action) != 1):
        print("Wrong number.")
        return 0

    victim = input("target:")

        
    if processThread.is_alive():
        print("putting it in queue")
        queue.put(customer + "|" + victim + "|" + action)
    else:
        queue.put(customer + "|" + victim + "|" + action)
        processThread.start()
        
    
    
def menu(orgs, spam_list, status, processThread,queue):
    org_index = 0
    spam_cl = ""
    
    while True:
        result = select(orgs, org_index, spam_list, spam_cl)
        if result[0] == 1:
            continue
        elif result[0] == 2:
            if processThread.is_alive():
                sub_block_spm(result[1].rstrip(),status,queue, processThread)
            else:
                processThread = Process(target=barracuda.main, args=(queue,))
                sub_block_spm(result[1].rstrip(),status,queue, processThread)
            continue
        else:
            print("Selected " + orgs[result[1]].name)
            sub_menu(orgs, org_index)
            
            
