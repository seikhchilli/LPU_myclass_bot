import pickle
from config_class import config
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import random
import myclass_credentials
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

pickle_obj = open("configuration.pickle", 'rb')
config_obj = pickle.load(pickle_obj)

if config_obj.userid == None or config_obj.password == None:
    userid, userpass = myclass_credentials.get_credentials()

options = Options()
options.add_experimental_option("excludeSwitches", ["enable-automation", 'enable-logging'])

prefs = {"credentials_enable_service": False, "profile.password_manager_enabled": False}
options.add_experimental_option("prefs", prefs)
options.add_argument('use-fake-ui-for-media-stream')

service = Service(executable_path=ChromeDriverManager().install())


driver = webdriver.Chrome(service = service, options=options)

try:
    banner_file = random.choice(os.listdir("banners"))
    banner = open('banners/' + banner_file, 'r')

    print('\n\n')
    print(banner.read())
    print('\n\n')
except:
    pass


print("\n**To change the configuration, run 'python config.py'\n")

driver.get("https://myclass.lpu.in/")

driver.implicitly_wait(5)

driver.maximize_window()

def get_current_time():
        t = time.localtime()
        return (time.strftime("%H:%M:%S", t))




#login
def myclasslogin():
    try:
        username = driver.find_element(by = By.NAME, value="i")
        password = driver.find_element(by = By.NAME, value = "p")
    except:
        print("No element found with name i or p")

    if config_obj.userid == None or config_obj.password == None:
        username.send_keys(userid) 
        password.send_keys(userpass)
        password.send_keys(Keys.RETURN)
    else:
        username.send_keys(config_obj.userid) 
        password.send_keys(config_obj.password)
        password.send_keys(Keys.RETURN)


    #select class option
    try:
        driver.find_element(by=By.LINK_TEXT, value="View Classes/Meetings").click()
    except:
        print("Class option not found")
    
    return time.time()

#get all the class links
def get_class_links():
    try:
        class_link_list = driver.find_elements(by=By.CLASS_NAME, value="fc-time-grid-event")
        return class_link_list
    except:
        print("No such element")

#get running class
def get_running_class(class_list):
        for i in class_list:
            style = i.get_attribute("style")
            if "background: green;" in style:
                return i

def answer_poll():
    poll_options = driver.find_elements(by = By.CLASS_NAME, value="pollButtonWrapper--Z12PRiw")

    if len(poll_options) != 0:
        print("\nPoll appeared at " + get_current_time())

        option = random.choice(poll_options)

        try:
            print("Option selected : ", end="")
            print(option.find_element(by = By.CLASS_NAME, value="button--Z2dosza").get_attribute("aria-label"))
        except:
            print("option unknown")

        option.click()


start_time = myclasslogin()
while True:
    running_class = None

    #wait for class to start
    
    while running_class == None:
        class_list = get_class_links()
        running_class = get_running_class(class_list)

        #if some class has started
        if running_class != None:
            running_class.click()
            break

        #refresh after 30 seconds
        for i in range(30):
            print("\rWaiting for class to start" + '.' * i + ' '*(30-i), end = "")
            time.sleep(1)
        
        time_elapsed = time.time() - start_time
        if time_elapsed > 900 :
            driver.refresh()
            start_time = time.time()
            if driver.title == "My Class Login - Lovely Professional University":
                myclasslogin()
    
    #join class
    try:
        driver.find_element(by = By.CLASS_NAME, value = "btn").click()

        print("\nJoined class at " + get_current_time())
    except:
        print("join button not found")

    waiting_for_class = driver.find_elements(by = By.ID, value = "joinCountDown")

    while len(waiting_for_class) != 0:
        time.sleep(120)
        waiting_for_class = driver.find_elements(by = By.ID, value ="joinCountDown")


    driver.switch_to.frame("frame")

    #select listen only mode
    try:
        if config_obj.listen_mode == '2':
            driver.find_element(by = By.XPATH, value = "//*[text()='Microphone']").click()
            time.sleep(3)
            driver.find_element(by = By.XPATH, value = "//*[text()='Yes']").click()
        else:
            driver.find_element(by = By.XPATH, value = "//*[text()='Listen only']").click()
    except:
        print("Listen only button not found.")

    if config_obj.poll_mode == '1':
        while True:
            #check if class is running
            class_running = driver.find_elements(by = By.CLASS_NAME, value="main--Z1w6YvE")

            if len(class_running) == 0:
                break

            
            for i in range(30):
                print("\rClass Running" + '.' * i + ' '*(30-i), end = "")
                time.sleep(1)
    else:
        while True:
            #check if class is running
            class_running = driver.find_elements(by = By.CLASS_NAME, value="main--Z1w6YvE")

            if len(class_running) == 0:
                break
            
            answer_poll()
            
            for i in range(30):
                print("\rClass Running" + '.' * i + ' '*(30-i), end = "")
                time.sleep(1)

    
    #class over
    print("Class over at " + get_current_time())

    try:
        driver.find_element(by = By.CLASS_NAME, value = "button--Z2dosza").click()
    except:
        print("ok button not found")

    #feedback
    stars = driver.find_elements(by = By.CLASS_NAME, value="jq-star")

    if len(stars) == 15:
        stars[4].click()
        stars[9].click()
        stars[14].click()

    try:
        driver.find_element(by = By.CLASS_NAME, value="btn").click()
    except:
        print("Submit not found")


    time.sleep(60)





    


