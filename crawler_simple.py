#!/usr/bin/env python3
# crawler_simple.py
import asyncio
from typing import Any, Dict, List
from crawl4ai.async_webcrawler import AsyncWebCrawler
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

def _stringify_links(links: Any) -> List[str]:
    if not links: return []
    if isinstance(links, dict):
        return [str(k) for k in links.keys()]
    if isinstance(links, (list, tuple, set)):
        out = []
        for item in links:
            if isinstance(item, str):
                out.append(item)
            elif isinstance(item, dict):
                for key in ("url", "href", "link"):
                    if key in item:
                        out.append(str(item[key]))
                        break
                else:
                    out.append(str(item))
            else:
                out.append(str(item))
        return out
    return [str(links)]

async def crawl_url(url: str) -> Dict[str, Any]:
    async with AsyncWebCrawler(verbose=False) as crawler:
        result = await crawler.arun(
            url=url,
            excluded_tags=["nav", "footer", "aside"],
            remove_overlay_elements=True,
            markdown_generator=DefaultMarkdownGenerator(
                content_filter=PruningContentFilter(threshold=0.5, threshold_type="fixed"),
            ),
        )
        text = ""
        if hasattr(result, "markdown") and getattr(result.markdown, "raw_markdown", None):
            text = result.markdown.raw_markdown
        elif hasattr(result, "content"):
            text = result.content or ""
        return {
            "text": text or "",
            "source_url": url
        }

if __name__ == "__main__":
    url = "https://www.bbc.com/news"
    data = asyncio.run(crawl_url(url))
    print(data["text"])
