from selenium import webdriver
from selenium.webdriver.common.by import By

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach",True)
driver = webdriver.Chrome(options=chrome_options)
driver.get("http://secure-retreat-92358.herokuapp.com/")

lname = driver.find_element(By.NAME,"lName")
fname = driver.find_element(By.NAME,"fName")
email = driver.find_element(By.NAME,"email")
submit_button = driver.find_element(By.XPATH,"/html/body/form/button")

lname.send_keys("Python")
fname.send_keys("Python")
email.send_keys("Python@gmail.com")
submit_button.click()


