from selenium import webdriver

from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox()

driver.get("https://www.simplilearn.com")

driver.find_element_by_xpath("//a[@title='Free Courses']").click()

driver.quit()
