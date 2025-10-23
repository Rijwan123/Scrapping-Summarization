#!/usr/bin/env python3
import os
from typing import Dict
from dotenv import load_dotenv
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

MODEL = "gpt-3.5-turbo"

def summarize_text(text: str, min_words: int = 20, max_words: int = 120) -> Dict[str, str]:
    if not text.strip():
        return {"summary": "", "original_length": 0, "summary_length": 0}

    prompt = f"Summarize the following text in {min_words}-{max_words} words:\n\n{text}"
    try:
        resp = openai.ChatCompletion.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        summary = resp["choices"][0]["message"]["content"].strip()
        return {
            "summary": summary,
            "original_length": len(text),
            "summary_length": len(summary),
        }
    except Exception as e:
        return {"summary": "", "original_length": len(text), "summary_length": 0, "error": str(e)}

if __name__ == "__main__":
    sample_text = "OpenAI provides powerful models for text summarization and other NLP tasks."
    print(summarize_text(sample_text))
