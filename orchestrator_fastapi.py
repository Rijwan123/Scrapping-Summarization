#!/usr/bin/env python3
import os
import time
import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from crawler_simple import crawl_url
from summarizer_simple import summarize_text
import uvicorn

app = FastAPI()

class Request(BaseModel):
    url: str

def fallback_summary(text: str, max_chars: int = 1000) -> str:
    """
    Return first N characters as fallback summary if the model fails or returns empty.
    Tries to cut at sentence boundary.
    """
    if not text:
        return ""
    text = text.strip()
    snippet = text[:max_chars]
    for sep in (". ", "!\n", "?\n", "\n"):
        idx = snippet.rfind(sep)
        if idx != -1 and idx > max_chars // 2:
            return snippet[: idx + len(sep)].strip()
    return snippet.strip() + "..."

@app.post("/summarize")
async def summarize_url(req: Request):
    if not req.url.strip():
        raise HTTPException(status_code=400, detail="Missing URL")

    start = time.time()
    try:
        # Step 1: Crawl
        crawl_result = await crawl_url(req.url)
        text = crawl_result.get("text", "").strip()
        print("scraped_data======", text[:1000] + ("..." if len(text) > 1000 else ""))
        if not text:
            raise HTTPException(status_code=500, detail="No text extracted from page")

        # Step 2: Summarize
        summary_raw = await asyncio.to_thread(summarize_text, text[:10000])
        print("Summarry----------", repr(summary_raw))

        # Step 3: Normalize summary
        if isinstance(summary_raw, dict):
            summary_text = summary_raw.get("summary", "").strip()
            summary_len = summary_raw.get("summary_length", len(summary_text))
        else:
            summary_text = str(summary_raw).strip()
            summary_len = len(summary_text)

        # Step 4: Fallback if summary empty
        if not summary_text:
            summary_text = fallback_summary(text)
            summary_len = len(summary_text)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "url": req.url,
        "summary": summary_text,
        "original_length": len(text),
        "summary_length": summary_len,
        "duration": round(time.time() - start, 2),
    }

if __name__ == "__main__":
    uvicorn.run("orchestrator_fastapi:app", host="0.0.0.0", port=8000, reload=True)




# #!/usr/bin/env python3
# import os, time, asyncio
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from crawler_simple import crawl_url
# from summarizer_simple import summarize_text
# import uvicorn
# app = FastAPI()

# class Request(BaseModel):
#     url: str

# @app.post("/summarize")
# async def summarize_url(req: Request):
#     if not req.url.strip():
#         raise HTTPException(status_code=400, detail="Missing URL")

#     start = time.time()
#     try:
#         # Step 1: Crawl
#         crawl_result = await crawl_url(req.url)
#         text = crawl_result.get("text", "")
#         print("scraped_data======",text)
#         if not text.strip():
#             raise HTTPException(status_code=500, detail="No text extracted from page")
#         # Step 2: Summarize
#         summary = await asyncio.to_thread(summarize_text, text[:10000])
#         print("Summarry----------",summary)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

#     return {
          
#             "summary": summary if isinstance(summary, str) else summary.get("summary", ""),
#             "original_length": len(text),
#             "summary_length": len(summary) if isinstance(summary, str) else summary.get("summary_length", 0),
#             "duration": round(time.time() - start, 2),
#     }


