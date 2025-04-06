import json
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BrowserConfig, CacheMode
from crawl4ai.extraction_strategy import JsonXPathExtractionStrategy
import random
from base64 import b64decode
from curl_cffi import requests as cureq

url = "https://allegro.pl/kategoria/laptopy-491"
schema = {
    "name":"Product names vai XPath"
    , "baseSelector": "//div[@id='search-results']//article"
    , "fields": {
        "name": "PRODUCT NAME",
        "selector": "//h2/a/text()",
        "type": "text"
    }
}

browser_cfg = BrowserConfig(
    browser_type="chromium",
    headless=False,
    viewport_width=2000,
    viewport_height=2000,
    user_agent="Mozilla/5.0 (Macintosh; U; Intel Mac OS X 7_8_7) AppleWebKit/534.46 (KHTML, like Gecko) Chrome/53.0.2407.293 Safari/603",
    proxy="https://52.183.8.192:3128"
)

run_cfg = CrawlerRunConfig(
    cache_mode=CacheMode.BYPASS,
    wait_for_images=True,
    screenshot=True,
    word_count_threshold=15,
    exclude_external_links=True,
    stream=True,
    magic=True,
    simulate_user=True,
    override_navigator=True,
    mean_delay=10,
    check_robots_txt=True,
    scan_full_page=True,
    scroll_delay=2
    #extraction_strategy=JsonXPathExtractionStrategy(schema, verbose=True)
)

async def extract_data():
    async with AsyncWebCrawler(verbose=True) as crawler:
        result = await crawler.arun(
            url=url,
            config=run_cfg
        )
    if not result.success:
        print("Crawl failed:", result.error_message)
        return
    with open("all.png", "wb") as f:
        f.write(b64decode(result.screenshot))
    # data = json.loads(result.extracted_content)
    # print(f"Extracted {len(data)} coin rows")
    # print(data)

asyncio.run(extract_data())

