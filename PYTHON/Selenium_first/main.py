from selenium import webdriver
from selenium.webdriver.common.by import By

chrome_driver_path = "D:\Projekty\Projekty_python\chromedriver-win64/chromedriver.exe"
driver = webdriver.Chrome()
driver.get("https://www.python.org/")

upcoming_events_names = [name.text for name in driver.find_elements(By.XPATH,'//*[@id="content"]/div/section/div[2]/div[2]/div/ul/li/a')]
upcoming_events_times = [time.text for time in driver.find_elements(By.XPATH,'//*[@id="content"]/div/section/div[2]/div[2]/div/ul/li/time')]
events = {i: {upcoming_events_times[i]:upcoming_events_names[i]} for i in range(len(upcoming_events_times))}

print(events)