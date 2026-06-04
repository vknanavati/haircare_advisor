# product_extractor.py
# ─────────────────────────────────────────────────────────────────────────────
# Takes raw Reddit text and uses Claude to extract haircare product names
# along with whether each product is recommended or warned against.
#
# Plain explanation:
#   This script sends the messy Reddit content to Claude with a precise
#   prompt asking it to identify every specific product name mentioned,
#   AND whether the community sentiment around that product is positive
#   (recommended) or negative (avoid). Claude returns a JSON list of
#   objects, which we parse and return as a Python list of dicts.
#
# Analogy:
#   Imagine handing a pile of Yelp reviews to a sharp assistant and saying
#   "go through all of this and write me a clean list of every restaurant
#   mentioned — but also tell me whether people loved it or hated it."
#   That's exactly what Claude does here. It doesn't just spot the names,
#   it understands the context around each one.
# ─────────────────────────────────────────────────────────────────────────────

import json                # for parsing Claude's JSON response into a Python list
import anthropic           # Anthropic's official Python client for Claude
from config import (       # import our constants
    ANTHROPIC_API_KEY,
    CLAUDE_MODEL,
    MAX_PRODUCTS_TO_RESEARCH,
)


def extract_products(reddit_text: str, user_query: str) -> list[dict]:
    """
    Sends Reddit text to Claude and extracts product names with sentiment.

    Plain explanation:
        Initializes the Anthropic client, constructs a prompt that gives
        Claude both the user's original query and the raw Reddit content,
        then asks it to return a JSON list of objects — each with a product
        name and a sentiment label of either 'positive' or 'negative'.
        We parse that JSON and return a clean Python list of dicts.

    Analogy:
        Like asking a movie critic to go through a stack of audience comment
        cards and pull out every film title mentioned — but also mark each
        one as thumbs up or thumbs down based on what the audience actually
        said about it. The name alone isn't enough; the verdict matters too.

    Args:
        reddit_text: the raw combined Reddit content from reddit_search.py
        user_query:  the original query the user typed, used for context

    Returns:
        a list of dicts like: [{"name": "Product X", "sentiment": "positive"}]
        capped at MAX_PRODUCTS_TO_RESEARCH entries
    """
    # initialize the Anthropic client with our API key
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    # construct the prompt — now explicitly asking for sentiment awareness
    prompt = f"""You are an expert at analyzing haircare community discussions.

The user is looking for: "{user_query}"

Below is content from Reddit haircare communities. Your job is to extract every specific haircare product name mentioned, along with whether the community sentiment around that product is positive or negative.

RULES:
- Return ONLY a valid JSON array of objects — no explanation, no preamble, no text outside the array
- Each object must have exactly two fields:
    "name": the full product name including brand (e.g. "Tresemme Heat Tamer Spray")
    "sentiment": either "positive" or "negative"
- Use "positive" when someone recommends, praises, loves, or has good results with a product
- Use "negative" when someone warns against, dislikes, had bad results with, or says to avoid a product
- If a product has mixed mentions (some love it, some hate it), include it TWICE — once as positive, once as negative — so the UI can flag it as controversial
- Do NOT include generic terms like "heat protectant spray" or "leave-in conditioner" — only specific named products with a brand
- If no specific named products are mentioned, return an empty array: []
- Maximum {MAX_PRODUCTS_TO_RESEARCH} objects total

REDDIT CONTENT:
{reddit_text}

Return only the JSON array now:"""

    # send the prompt to Claude and get a response
    message = client.messages.create(
        model=CLAUDE_MODEL,       # which Claude model to use
        max_tokens=1024,          # maximum length of Claude's response
        messages=[
            {
                "role": "user",       # this message is from the user
                "content": prompt     # the full prompt we constructed above
            }
        ]
    )

    # extract the text content from Claude's response
    response_text = message.content[0].text.strip()

    # Claude sometimes wraps JSON in ```json code fences even when asked not to
    # strip those out so json.loads() can parse the raw JSON cleanly
    if response_text.startswith("```"):
        # remove the opening fence (```json or just ```)
        response_text = response_text.split("\n", 1)[1]
    if response_text.endswith("```"):
        # remove the closing fence
        response_text = response_text.rsplit("```", 1)[0]

    # strip again after removing fences
    response_text = response_text.strip()

    # parse the JSON string Claude returned into a Python list of dicts
    try:
        products = json.loads(response_text)  # convert JSON string to Python list

        # make sure we got a list back
        if not isinstance(products, list):
            print("Claude returned unexpected format — expected a list")
            return []

        # validate each item has the fields we expect
        validated = []
        for item in products:
            # each item must be a dict with 'name' and 'sentiment' keys
            if isinstance(item, dict) and "name" in item and "sentiment" in item:
                # normalize sentiment to lowercase just in case Claude varies casing
                item["sentiment"] = item["sentiment"].lower()
                # only accept valid sentiment values
                if item["sentiment"] in ("positive", "negative"):
                    validated.append(item)

        # cap at our maximum and return
        return validated[:MAX_PRODUCTS_TO_RESEARCH]

    except json.JSONDecodeError as e:
        # log the error and return empty list if parsing fails
        print(f"Failed to parse Claude's response as JSON: {e}")
        print(f"Claude returned: {response_text}")
        return []


# ─────────────────────────────────────────────────────────────────────────────
# Test block — runs only when you execute this file directly
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    from reddit_search import search_reddit

    test_query = "heat protectants for fine thick hair blow drying"

    print(f"Step 1: Searching Reddit for '{test_query}'...")
    reddit_text = search_reddit(test_query)

    if not reddit_text:
        print("No Reddit content found — cannot extract products.")
    else:
        print(f"Found Reddit content ({len(reddit_text)} characters)")
        print("\nStep 2: Extracting products with sentiment using Claude...")
        products = extract_products(reddit_text, test_query)

        print(f"\nProducts found ({len(products)}):")

        positive = [p for p in products if p["sentiment"] == "positive"]
        negative = [p for p in products if p["sentiment"] == "negative"]

        print(f"\n✅ Recommended ({len(positive)}):")
        for p in positive:
            print(f"   • {p['name']}")

        print(f"\n⚠️  Avoid ({len(negative)}):")
        for p in negative:
            print(f"   • {p['name']}")