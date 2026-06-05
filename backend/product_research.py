# product_research.py
# ─────────────────────────────────────────────────────────────────────────────
# For each product extracted from Reddit, searches the web for reviews
# and information, then uses Claude to synthesize a structured summary.
#
# Plain explanation:
#   This script takes the list of products from product_extractor.py,
#   searches the web for each one using Tavily, and sends those search
#   results to Claude asking it to return a structured JSON summary with
#   pros, cons, best-for notes, price range, and a verdict. This is the
#   final intelligence step before the data reaches the frontend.
#
# Analogy:
#   Think of this as a product reviewer whose job is to research each
#   item on a shopping list. For every product, they read the reviews
#   from multiple sources, then write a concise, structured report card
#   — pros, cons, who it's best for, and what it costs. Claude is the
#   reviewer, Tavily is the research tool, and the report card is the
#   JSON summary we send to the frontend.
# ─────────────────────────────────────────────────────────────────────────────

import json
import time               # for parsing Claude's JSON response
import anthropic           # Anthropic's official Python client
from tavily import TavilyClient  # Tavily's search client
from config import (
    ANTHROPIC_API_KEY,
    TAVILY_API_KEY,
    CLAUDE_MODEL,
    PRODUCT_SEARCH_RESULTS,
)


def research_product(product: dict) -> dict:
    """
    Researches a single product and returns a structured summary.

    Plain explanation:
        Takes a product dict with 'name' and 'sentiment' fields, searches
        the web for reviews and information about that product, sends those
        results to Claude, and returns a rich structured summary dict.

    Analogy:
        Like sending a researcher to find everything written about one
        specific product — then having an expert editor read all of it
        and distill it into a single, clean one-page brief. You get the
        essential information without having to read everything yourself.

    Args:
        product: dict with 'name' (str) and 'sentiment' (str) fields

    Returns:
        a dict with full product research — name, sentiment, pros, cons,
        best_for, price_range, verdict, and controversial flag
    """
    product_name = product["name"]        # the product name string
    reddit_sentiment = product["sentiment"]  # 'positive' or 'negative' from Reddit

    # ── Step 1: Search the web for this product ───────────────────────────────
    tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

    try:
        # search for reviews and information about this specific product
        search_response = tavily_client.search(
            query=f"{product_name} haircare review pros cons",
            max_results=PRODUCT_SEARCH_RESULTS,
            search_depth="advanced",
            include_answer=False,
        )

        # collect all the content from search results into one block of text
        search_results = []
        for result in search_response.get("results", []):
            content = result.get("content", "")
            title   = result.get("title", "")
            if content:
                search_results.append(f"SOURCE: {title}\nCONTENT: {content}")

        # join all results into one string for Claude to read
        research_text = "\n\n".join(search_results)

    except Exception as e:
        print(f"Tavily search failed for '{product_name}': {e}")
        research_text = ""  # proceed with empty research if search fails

    # ── Step 2: Ask Claude to synthesize the research ─────────────────────────
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

        # strip code fences FIRST before any other cleanup
        # Claude wraps JSON in ```json ... ``` despite being told not to
        # we strip the opening fence line and closing fence line
        lines = response_text.splitlines()          # split into individual lines
        if lines and lines[0].startswith("```"):    # if first line is a fence
            lines = lines[1:]                       # remove the opening fence line
        if lines and lines[-1].strip() == "```":    # if last line is a closing fence
            lines = lines[:-1]                      # remove the closing fence line
        response_text = "\n".join(lines).strip()    # rejoin into a clean string

        # parse Claude's JSON response into a Python dict
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
    Researches every product in the list and returns all summaries.

    Plain explanation:
        Loops through every product dict, calls research_product() on each
        one, collects the results, and returns them all as a list. This is
        the function that app.py will call.

    Analogy:
        Like handing a stack of product names to a team of reviewers —
        one reviewer per product — and collecting all their report cards
        when they're done. Each reviewer works on one product; this
        function coordinates the whole team.

    Args:
        products: list of dicts with 'name' and 'sentiment' fields

    Returns:
        list of structured product summary dicts
    """
    results = []  # will hold all the research summaries

    for i, product in enumerate(products):
        print(f"  Researching {i+1}/{len(products)}: {product['name']}...")
        summary = research_product(product)  # research this one product
        results.append(summary)
        time.sleep(2)              # add its summary to our list

    return results  # return all summaries together


# ─────────────────────────────────────────────────────────────────────────────
# Test block — runs only when you execute this file directly
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    from reddit_search import search_reddit
    from product_extractor import extract_products

    test_query = "heat protectants for fine thick hair blow drying"

    print(f"Step 1: Searching Reddit for '{test_query}'...")
    reddit_text = search_reddit(test_query)
    print(f"Found Reddit content ({len(reddit_text)} characters)")

    print("\nStep 2: Extracting products with sentiment...")
    products = extract_products(reddit_text, test_query)
    print(f"Found {len(products)} products")

    print("\nStep 3: Researching each product...")
    summaries = research_all_products(products)

    print("\n" + "=" * 60)
    print("FINAL RESULTS")
    print("=" * 60)

    for s in summaries:
        print(f"\n{'⚠️  AVOID' if s['reddit_sentiment'] == 'negative' else '✅ RECOMMENDED'}: {s['name']}")
        if s.get("controversial"):
            print("   ⚡ CONTROVERSIAL — mixed reviews")
        print(f"   Best for: {s.get('best_for', 'N/A')}")
        print(f"   Price: {s.get('price_range', 'N/A')}")
        print(f"   Pros: {', '.join(s.get('pros', []))}")
        print(f"   Cons: {', '.join(s.get('cons', []))}")
        print(f"   Verdict: {s.get('verdict', 'N/A')}")