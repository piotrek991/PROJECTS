import asyncio
import json
import os
from typing import List

from crawl4ai import AsyncWebCrawler, BrowserConfig, CacheMode, CrawlerRunConfig
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from pydantic import BaseModel, Field
from dotenv import load_dotenv, dotenv_values

load_dotenv()
URL_TO_SCRAPE = "https://www.nbcnews.com/business"

INSTRUCTION_TO_LLM = "Extract entities and relationships from the content. Return valid JSON."

class Product(BaseModel):
    name: str
    price: str


async def main():
    llm_strategy = LLMExtractionStrategy(
        provider="groq/deepseek-r1-distill-llama-70b",
        api_token=os.getenv("GROQ_API_KEY"),
        schema=Product.model_json_schema(),
        extraction_type="schema",
        instruction=INSTRUCTION_TO_LLM,
        chunk_token_threshold=1000,
        overlap_rate=0.0,
        apply_chunking=True,
        input_format="html",
        extra_args={"temperature": 0.0, "max_tokens": 5000},
    )

    crawl_config = CrawlerRunConfig(
        extraction_strategy=llm_strategy,
        cache_mode=CacheMode.BYPASS
    )

    browser_cfg = BrowserConfig(browser_type="chromium", headless=True, verbose=True)

    async with AsyncWebCrawler(config=browser_cfg) as crawler:

        result = await crawler.arun(url=URL_TO_SCRAPE, config=crawl_config)

        if result.success:
            data = json.loads(result.extracted_content)

            print("Extracted items:", data)

            llm_strategy.show_usage()
        else:
            print("Error:", result.error_message)


if __name__ == "__main__":
    asyncio.run(main())
