from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from lxml import etree


def get_data() -> BeautifulSoup:
    ch_options = webdriver.ChromeOptions()

    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    ch_options.add_argument(f'user-agent={user_agent}')
    ch_options.add_argument('no-sandbox')
    ch_options.add_argument('allow-running-insecure-content')
    ch_options.add_argument('disable-gpu')
    ch_options.add_argument("headless")

    driver = webdriver.Chrome(options=ch_options)
    driver.get("https://www.otomoto.pl/osobowe?search%5Border%5D=created_at_first%3Adesc")
    soup_inner = BeautifulSoup(driver.page_source, 'html.parser')

    driver.quit()
    return soup_inner


if __name__ == '__main__':

    site_data = get_data()
    dom = etree.HTML(str(site_data))
    search_data = dom.xpath("//div[@data-testid='search-results']/div/article")

    for num, el in enumerate(dom.xpath("//div[@data-testid='search-results']/div/article")):
        #advertisement_name = el.find_element(By.XPATH
        #               , ".//div[not(@id='financing-widget-listing-card-entrypoint')]/*/a[@target='_self']")
        # print("soup search")
        dom_inner = etree.HTML(str(el.text))
        print(el.xpath(".//div[not(@id='financing-widget-listing-card-entrypoint')]/*/a[@target='_self']")[0].text)
        # #print(soup.prettify())
        # print("selenium search")
        # print(advertisement_name.get_attribute('outerHTML'))
        if num > 0:
            break




