# product_research.py
import json
import anthropic
from tavily import TavilyClient
from concurrent.futures import ThreadPoolExecutor, as_completed
from config import (
    ANTHROPIC_API_KEY,
    TAVILY_API_KEY,
    CLAUDE_MODEL,
    PRODUCT_SEARCH_RESULTS,
)


def research_product(product: dict) -> dict:
    product_name     = product["name"]
    reddit_sentiment = product["sentiment"]

    tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

    try:
        search_response = tavily_client.search(
            query=f"{product_name} haircare review pros cons",
            max_results=PRODUCT_SEARCH_RESULTS,
            search_depth="advanced",
            include_answer=False,
        )
        search_results = []
        for result in search_response.get("results", []):
            content = result.get("content", "")
            title   = result.get("title", "")
            if content:
                search_results.append(f"SOURCE: {title}\nCONTENT: {content}")
        research_text = "\n\n".join(search_results)

    except Exception as e:
        print(f"Tavily search failed for '{product_name}': {e}")
        research_text = ""

    anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    prompt = f"""You are an expert haircare product reviewer.

Product to research: "{product_name}"
Reddit community sentiment: {reddit_sentiment}

Below is web research about this product. Synthesize it into a structured summary.

RULES:
- Return ONLY a valid JSON object — no explanation, no preamble, no code fences
- The JSON must have exactly these fields:
    "name": the product name (string)
    "brand": the brand name extracted from the product name (string)
    "reddit_sentiment": "{reddit_sentiment}" (keep as-is)
    "controversial": true if you find strongly mixed reviews, false otherwise (boolean)
    "pros": list of 2-4 specific benefits people mention (array of strings)
    "cons": list of 1-3 specific drawbacks people mention (array of strings)
    "best_for": a short phrase describing who this product works best for (string)
    "price_range": approximate price range like "$8-12" or "$25-30" — use "$?" if unknown (string)
    "verdict": one sentence summarizing whether to buy this and why (string)

WEB RESEARCH:
{research_text if research_text else "No web research available — use your general knowledge."}

Return only the JSON object now:"""

    try:
        message = anthropic_client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )

        response_text = message.content[0].text.strip()

        lines = response_text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        response_text = "\n".join(lines).strip()

        summary = json.loads(response_text)
        return summary

    except json.JSONDecodeError as e:
        print(f"Failed to parse Claude response for '{product_name}': {e}")
        return {
            "name": product_name,
            "brand": "",
            "reddit_sentiment": reddit_sentiment,
            "controversial": False,
            "pros": [],
            "cons": [],
            "best_for": "Unknown",
            "price_range": "$?",
            "verdict": "Research unavailable for this product.",
        }

    except Exception as e:
        print(f"Claude call failed for '{product_name}': {e}")
        return {
            "name": product_name,
            "brand": "",
            "reddit_sentiment": reddit_sentiment,
            "controversial": False,
            "pros": [],
            "cons": [],
            "best_for": "Unknown",
            "price_range": "$?",
            "verdict": "Research unavailable for this product.",
        }


def research_all_products(products: list[dict]) -> list[dict]:
    """
    Researches all products simultaneously using parallel threads.

    Plain explanation:
        Instead of researching products one at a time, this function
        launches all research calls at the same time using a thread pool.
        Each thread handles one product independently and we collect
        results as threads finish, reassembled in the original order.

    Analogy:
        Old approach: one chef cooking 6 dishes back to back.
        New approach: 6 chefs cooking simultaneously — total time is
        roughly the time for the slowest single dish, not the sum of all.
        ThreadPoolExecutor is the kitchen manager assigning one chef per dish.
    """
    results = {}

    with ThreadPoolExecutor(max_workers=6) as executor:
        future_to_index = {
            executor.submit(research_product, product): i
            for i, product in enumerate(products)
        }

        for future in as_completed(future_to_index):
            index        = future_to_index[future]
            product_name = products[index]["name"]

            try:
                results[index] = future.result()
                print(f"  ✓ Finished: {product_name}")
            except Exception as e:
                print(f"  ✗ Failed: {product_name} — {e}")
                results[index] = {
                    "name": product_name,
                    "brand": "",
                    "reddit_sentiment": products[index]["sentiment"],
                    "controversial": False,
                    "pros": [],
                    "cons": [],
                    "best_for": "Unknown",
                    "price_range": "$?",
                    "verdict": "Research unavailable for this product.",
                }

    return [results[i] for i in sorted(results.keys())]


if __name__ == "__main__":
    import time
    from reddit_search import search_reddit
    from product_extractor import extract_products

    test_query = "heat protectants for fine thick hair blow drying"

    print(f"Step 1: Searching Reddit for '{test_query}'...")
    reddit_text = search_reddit(test_query)
    print(f"Found Reddit content ({len(reddit_text)} characters)")

    print("\nStep 2: Extracting products with sentiment...")
    products = extract_products(reddit_text, test_query)
    print(f"Found {len(products)} products")

    print(f"\nStep 3: Researching {len(products)} products IN PARALLEL...")
    start = time.time()
    summaries = research_all_products(products)
    elapsed = time.time() - start
    print(f"Completed in {elapsed:.1f} seconds")

    for s in summaries:
        print(f"\n{'⚠️  AVOID' if s['reddit_sentiment'] == 'negative' else '✅ RECOMMENDED'}: {s['name']}")
        print(f"   Verdict: {s.get('verdict', 'N/A')}")
