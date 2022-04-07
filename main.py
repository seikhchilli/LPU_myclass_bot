import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import random
import myclass_credentials
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


userid, userpass = myclass_credentials.get_credentials()

options = Options()
options.add_experimental_option("excludeSwitches", ["enable-automation", 'enable-logging'])

prefs = {"credentials_enable_service": False, "profile.password_manager_enabled": False}
options.add_experimental_option("prefs", prefs)

service = Service(executable_path=ChromeDriverManager().install())


driver = webdriver.Chrome(service = service, options=options)


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

    username.send_keys(userid) 
    password.send_keys(userpass)
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
        driver.find_element(by = By.XPATH, value = "//*[text()='Listen only']").click()
    except:
        print("Listen only button not found.")

    poll_options_count = 0
    while True:
        #check if class is running
        class_running = driver.find_elements(by = By.CLASS_NAME, value="main--Z1w6YvE")

        if len(class_running) == 0:
            break

            

        poll_options = driver.find_elements(by = By.CLASS_NAME, value="pollButtonWrapper--Z12PRiw")

        if len(poll_options) != 0:
            print("\nPoll appeared at " + get_current_time())
            poll_options_count += 1

            option = random.choice(poll_options)

            try:
                print("Option selected : ", end="")
                print(option.find_element(by = By.CLASS_NAME, value="button--Z2dosza").get_attribute("aria-label"))
            except:
                print("option unknown")

            option.click()
        
        for i in range(30):
            print("\rClass Running" + '.' * i + ' '*(30-i), end = "")
            time.sleep(1)
    
    #class over
    print("\nTotal numbers of poll appeared : " + str(poll_options_count))
    print("class over at " + get_current_time())

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





    


