🚀🤖 Crawl4AI: Open-source LLM Friendly Web Crawler & Scraper.
unclecode%2Fcrawl4ai | Trendshift

GitHub Stars GitHub Forks

PyPI version Python Version Downloads GitHub Sponsors

Follow on X Follow on LinkedIn Join our Discord

Crawl4AI turns the web into clean, LLM ready Markdown for RAG, agents, and data pipelines. Fast, controllable, battle tested by a 50k+ star community.


Why developers pick Crawl4AI:
    LLM ready output, smart Markdown with headings, tables, code, citation hints
    Fast in practice, async browser pool, caching, minimal hops
    Full control, sessions, proxies, cookies, user scripts, hooks
    Adaptive intelligence, learns site patterns, explores only what matters
    Deploy anywhere, zero keys, CLI and Docker, cloud friendly

🚀 Quick Start
1. Install Crawl4AI:
# Install the package
pip install -U crawl4ai

# For pre release versions
pip install crawl4ai --pre

# Run post-installation setup
crawl4ai-setup

# Verify your installation
crawl4ai-doctor
If you encounter any browser-related issues, you can install them manually:

    python -m playwright install --with-deps chromium

2. Run a simple web crawl with Python:

    import asyncio
    from crawl4ai import *

    async def main():
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(
                url="https://www.nbcnews.com/business",
            )
            print(result.markdown)

    if __name__ == "__main__":
        asyncio.run(main())

3. Or use the new command-line interface:
# Basic crawl with markdown output
crwl https://www.nbcnews.com/business -o markdown

# Deep crawl with BFS strategy, max 10 pages
crwl https://docs.crawl4ai.com --deep-crawl bfs --max-pages 10

# Use LLM extraction with a specific question
crwl https://www.example.com/products -q "Extract all product prices"