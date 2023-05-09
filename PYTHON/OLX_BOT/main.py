from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://www.olx.pl/praca/")
driver.implicitly_wait(20)

driver.find_element(By.XPATH,"//div/button[@id='onetrust-accept-btn-handler']").click()
driver.implicitly_wait(200)
driver.find_element(By.XPATH,'//div[@class="filter-item rel filter-item-contract"]').click()
driver.implicitly_wait(100)
list_el = driver.find_elements(By.XPATH,'//div[@class="filter-item rel filter-item-contract filterActive"]/ul/li[@class="dynamic clr brbott-4 "]')

for el in list_el:
    if(el.text == "Umowa o dzieło"):
        el.click()
        break
driver.find_element(By.XPATH,'//div[@class="filter-item rel filter-item-type"]').click()
driver.implicitly_wait(100)
list_el = driver.find_elements(By.XPATH,'//div[@class="filter-item rel filter-item-type filterActive"]/ul/li[@class="dynamic clr brbott-4 "]')

for el in list_el:
    if(el.text == "Pełny etat"):
        el.click()
        break



