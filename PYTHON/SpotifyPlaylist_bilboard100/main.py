import requests
from bs4 import BeautifulSoup

date = input("Input the date in format YYYY-MM-DD :")
link = "https://www.billboard.com/charts/hot-100/"+date+"/"
response = requests.get(link).text

soup = BeautifulSoup(response,"html.parser")
#lambda x: "c-label" and "a-no-trucate" in x.split() if x != "None" else "None"
text = "c-label  a-no-trucate a-font-primary-s lrv-u-font-size-14@mobile-max u-line-height-normal@mobile-max u-letter-spacing-0021 lrv-u-display-block a-truncate-ellipsis-2line u-max-width-330 u-max-width-230@tablet-only u-font-size-20@tablet"
data = (lambda x: x and "c-label" and "a-no-trucate" in x.split() if x is not None else False)(text)
for item in soup.find_all(class_ = True):
    print(item['class'])
