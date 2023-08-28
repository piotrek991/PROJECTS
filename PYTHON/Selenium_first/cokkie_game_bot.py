from seleniumwire import webdriver


def request_interceptor(request):
    print(request.headers)
    del request.headers["user-agent"]
    request.headers["user-agent"] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    del request.headers["sec-ch-ua"]
    request.headers["sec-ch-ua"] = '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"'
    request.headers["referer"] = 'https://www.google.com'

dict_headers = {
    'Referer:':'https://www.google.com',
    'Sec-Ch-Ua:':'"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
    'User-Agent:':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
}
driver = webdriver.Chrome()
driver.request_interceptor = request_interceptor

driver.get('https://orteil.dashnet.org/cookieclicker')



