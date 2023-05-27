from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
from pyotp import *
import sys
import contextlib

repeat = False
#initialize the browser
def init(queue):

    temp = queue.get()
    temp = temp.split("|")
    action = temp[2]
    victim = temp[1]
    customer = temp[0]
    #print("initing ", customer , " " , action , " " , victim)
    options = Options()
    ser = Service("chromedriver.exe")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(service=ser, options = options)

    delay = 10
    totp = TOTP("") #CHANGE THIS
    driver.get("https://manage.barracudamsp.com/Login.aspx?ReturnUrl=%2f")
    driver.maximize_window()
    login(driver,delay,totp,action,customer,queue,victim)
    

def idle(queue,driver):
    
    
    while True:

        time.sleep(10)
        try:
            driver.get("https://ess.barracudanetworks.com/settings/sender_policies")
        except Exception:
            sys.exit()

        if queue.empty():
            print("dddd")
        else:
            repeat = True
            temp = queue.get()
            temp = temp.split("|")
            perform(driver,10,temp[2],temp[0],queue,temp[1])

            
        
    


#action function
def add(driver,action,customer,queue,victim):
    delay = 1
    myElem = WebDriverWait(driver,delay).until(EC.presence_of_element_located((By.NAME, "sp_email")))
    driver.find_element(By.NAME, "sp_email").send_keys(victim)

    select = Select(driver.find_element(By.ID, "sp_policy"))
    print(select.options)
    if (int(action) == 1):
        select.select_by_value("block")
    elif (int(action) == 2):
        select.select_by_value("exempt")
    tries = 3
    for i in range(tries):
        try:
            driver.find_element(By.XPATH, "//a[@title='Add']").click()
            myElem = WebDriverWait(driver,delay).until(EC.presence_of_element_located((By.NAME, "sp_email")))
            break
        except TimeoutException:
            print("Timed out")

    if repeat == False:
        idle(queue,driver)


#perform the action
def perform(driver,delay,action,customer,queue,victim):
    try:
        driver.get("https://manage.barracudamsp.com/SSOHandoff.aspx?type=bcc")
        myElem2 = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, "hui-account-dropdown")))
        driver.find_element(By.ID, 'hui-account-dropdown').click()
        time.sleep(0.85)
        driver.find_element(By.XPATH, "//*[contains(text()," + " '" + customer + "')]").click()
        myElem3 = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, "hui-account-dropdown")))
        time.sleep(0.5)
        driver.get("https://ess.barracudanetworks.com/settings/sender_policies")
        myElem4 = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-title="Domains"]')))
        add(driver,action,customer,queue,victim)
        
    except TimeoutException:
        print("Perform failed 1")
        perform(driver,delay,action,customer)
#Try to login
def login(driver,delay,totp,action,customer,queue,victim):
    with contextlib.redirect_stdout(None):
    
        try:
            myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'ctl00_start_LoginForm1_txtUserName')))
            driver.find_element(By.ID, "ctl00_start_LoginForm1_txtUserName").send_keys("") #change this
            driver.find_element(By.ID, "ctl00_start_LoginForm1_txtPassword").send_keys("")  #and this
            driver.find_element(By.ID, "ctl00_start_LoginForm1_LoginButton").click()

            try:
                token = totp.now()
                myElem2 = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, "ctl00_start_txtAuthenticationCode")))
                driver.find_element(By.ID, "ctl00_start_txtAuthenticationCode").send_keys(token)
                driver.find_element(By.ID, "ctl00_start_btnAuthenticate").click()
                myElem2 = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, "ctl00_ContentMain_Repeater1_ctl00_HyperLink1")))
                perform(driver,delay,action,customer,queue,victim)
            except TimeoutException:
                print("failed to load(nested)")
        except TimeoutException:
            print("failed to load(inside)")

#main control
def main(queue):
    init(queue)









