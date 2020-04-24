from selenium import webdriver

driver = webdriver.Firefox('/usr/bin/')
driver.get("https://ttsdemo.com/")

elem = driver.find_element_by_class_name('textarea-clone')
