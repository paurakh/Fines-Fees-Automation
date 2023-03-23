from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import select 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re 
import time 


OK_DOC = ""
first_name = ""
last_name = ""
dob = ""

def get_input(): 

    #set regular expressions for input validation
    ok_doc_regex = re.compile(r'\d{6}+$')
    name_regex = re.compile(r'[a-zA-Z]+$')
    dob_regex = re.compile(r'\d{2}/\d{2}/\d{4}+$')

    #get input from user 
    OK_DOC = input("Enter the DOC number: ")
    first_name = input("Enter the first name: ")
    last_name = input("Enter the last name: ")
    dob = input("Enter the date of birth (MM/DD/YYYY): ") 

    #validate input
    if not ok_doc_regex.match(OK_DOC):
        print("Please enter a valid DOC number")
    if not name_regex.match(first_name):
        print("Please enter a valid first name")
    if not name_regex.match(last_name):
        print("Please enter a valid last name")
    if not dob_regex.match(dob):
        print("Please enter a valid date of birth (MM/DD/YYYY)")

    return OK_DOC, first_name, last_name, dob
    
def open_browser(): 

    #open browser
    PATH = "/Users/paurakh/Downloads/chromedriver"
    service = Service(PATH)
    driver = webdriver.Chrome(service=service)
    driver.get("https://okoffender.doc.ok.gov/")


    # selecting the accept button  
    disclaimer_button = driver.find_element(by=By.ID, value="cphMain_cmdAcceptDisclaimer")
    disclaimer_button.click()



    # enter search criteria 
    doc_box = driver.find_element(by=By.XPATH, value = '//*[@id="cphMain_txtDOCNum"]' )
    doc_box.send_keys(OK_DOC)

    first_name_box = driver.find_element(by=By.XPATH, value='//*[@id="cphMain_txtFirstName"]')
    first_name_box.send_keys(first_name)

    last_name_box = driver.find_element(by=By.XPATH, value='//*[@id="cphMain_txtLastName"]')
    last_name_box.send_keys(last_name)

    dob_box = driver.find_element(by=By.XPATH, value='//*[@id="cphMain_txtDOB"]')
    dob_box.send_keys(dob)


    #checking if captcha has been completed 

    
    time.sleep(10)

    #clicking the search button 
    search_button = driver.find_element(by=By.XPATH, value='//*[@id="cphMain_cmdBasicSearch"]')
    search_button.click()
    
    #wait for page to load 
    time.sleep(10)
    
    

    
   

def main():

    global OK_DOC, first_name, last_name, dob

    OK_DOC, first_name, last_name, dob = get_input()


    open_browser()

if __name__ == "__main__": 
    main()





####


#id="cphMain_txtFirstName"
#id="cphMain_txtLastName"
#id="cphMain_txtDOB"
#class="recaptcha-checkbox-checkmark"
#id="cphMain_cmdBasicSearch" 

####

 #computer enters search criteria into the boxes 
    # ActionChains(driver)\
    #     .move_to_element(first_name_box)\
    #     .click()\
    #     .send_keys(first_name)\
    #     .move_to_element(last_name_box)\
    #     .click()\
    #     .send_keys(last_name)\
    #     .move_to_element(dob_box)\
    #     .click()\
    #     .send_keys(dob)\
    #     .move_to_element(search_button)\
    #     .click()\
    #     .perform()
    

###




###


""" 232065
Enter the first name: jeffrey
Enter the last name: thomas
Enter the date of birth (MM/DD/YYYY): 12/27/1973 """
