import asyncio
import os
from dotenv import load_dotenv
import sys

from deep_research import FirecrawlApp  # adjust import path if FirecrawlApp is elsewhere

sys.stdout.reconfigure(encoding='utf-8')

async def test_firecrawl():
    load_dotenv()

    #print("FIRECRAWL_KEY =", os.getenv("FIRECRAWL_KEY"))
    #print("FIRECRAWL_BASE_URL =", os.getenv("FIRECRAWL_BASE_URL"))

    firecrawl = FirecrawlApp(
        api_key=os.getenv("FIRECRAWL_KEY", ""),
        base_url=os.getenv("FIRECRAWL_BASE_URL", "https://api.firecrawl.dev/v1")
    )

    result = await firecrawl.search("AI in ecology")
    print("\nFirecrawl result:\n", result)

if __name__ == "__main__":
    asyncio.run(test_firecrawl())
