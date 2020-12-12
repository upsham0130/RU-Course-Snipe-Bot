from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time


capabilities = DesiredCapabilities.CHROME
capabilities['goog:loggingPrefs'] = { 'browser':'ALL' }

driver = webdriver.Chrome(desired_capabilities=capabilities)
semester = ""

def main():
    driver.get('https://cas.rutgers.edu/login?service=https%3A%2F%2Fsims.rutgers.edu%2Fwebreg%2Fj_spring_cas_security_check')
    usr = driver.find_element_by_id("username")
    usr.send_keys(input("NetID: "))
    pwd = driver.find_element_by_id("password")
    pwd.send_keys(input("Password: "))
    section1 = input("Index of Section 1: ")
    section2 = input("Index of Section 2: ")
    section3 = input("Index of Section 3: ")
    driver.find_element_by_name("submit").click()
    driver.find_element_by_name("submit").click()



    driver.get('https://sims.rutgers.edu/webreg/courseLookup.htm?_flowId=lookup-flow')

    WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.ID,"iframe2")))
    driver.find_element_by_id("campus_NB").click()
    driver.find_element_by_id("level_U").click()
    driver.find_element_by_id("continueButton").click()

    # print console log messages
    time.sleep(5)
    semester = driver.execute_script("return AppData.selectedSemester;")
    array = driver.execute_script("return AppData.openSections;")
    while section1 not in array or section2 not in array or section3 not in array:
        time.sleep(1)
        driver.execute_script("CourseDownloadService.downloadCourses();")
        array = driver.execute_script("return AppData.openSections;")

    section = ""
    if section1 in array: section = section1
    elif section2 in array: section = section2
    else: section = section3
    sniped = snipe(section)

    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    driver.close()


def snipe(section) -> bool:
    driver.execute_script("window.open()")

    # Switch to the newly opened tab
    driver.switch_to.window(driver.window_handles[1])

    # Navigate to new URL in new tab
    driver.get("http://sims.rutgers.edu/webreg/editSchedule.htm?login=cas&semesterSelection=" + semester + "&indexList=" + section)
    driver.find_element_by_id("submit").click()
    sniped_complete = False
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'info')))
    try:
        error_message = driver.find_element_by_class_name("error").text
    except:
        sniped_complete = True
    
    if sniped_complete:
        print("Succesfully sniped " + section + "!")
        return True
    else:
        print("The following error occured: ")
        print(error_message)
        return False

main()