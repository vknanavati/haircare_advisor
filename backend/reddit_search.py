# reddit_search.py
# ─────────────────────────────────────────────────────────────────────────────
# Searches Reddit for posts and comments relevant to a haircare query.
# Uses Tavily's search API with site:reddit.com targeting to pull real
# community discussions without needing direct Reddit API access.
#
# Plain explanation:
#   This script takes a user's query, constructs targeted search strings
#   that point Tavily at specific subreddits, runs those searches, and
#   returns the raw text content of what it finds. It's the first step
#   in the pipeline — gathering the raw community intelligence.
#
# Analogy:
#   Think of this as a research assistant whose only job is to go to the
#   library (Reddit), find the most relevant discussions on the shelves
#   (subreddits), and bring back photocopies of the pages (raw text).
#   They don't interpret anything yet — they just collect.
# ─────────────────────────────────────────────────────────────────────────────

from tavily import TavilyClient  # Tavily's official Python client for search
from config import (             # import our constants from config.py
    TAVILY_API_KEY,
    TARGET_SUBREDDITS,
    REDDIT_MAX_RESULTS,
)


def build_reddit_queries(user_query: str) -> list[str]:
    """
    Builds a list of targeted search queries for each subreddit.

    Plain explanation:
        Takes the user's raw query and wraps it in site-specific search
        strings that tell Tavily to look only within particular subreddits.

    Analogy:
        Like telling a librarian "find me discussions about heat protectants,
        but only look in the science journals, beauty magazines, and
        haircare newsletters — not everywhere."

    Args:
        user_query: the raw query string the user typed in the frontend

    Returns:
        a list of search query strings, one per target subreddit
    """
    queries = []  # start with an empty list we'll fill up

    for subreddit in TARGET_SUBREDDITS:
        # construct a query that targets a specific subreddit
        # site:reddit.com/r/subredditname tells Tavily to only search there
        query = f"site:reddit.com/r/{subreddit} {user_query}"
        queries.append(query)  # add this query to our list

    return queries  # return the full list of targeted queries


def search_reddit(user_query: str) -> str:
    """
    Searches targeted subreddits for the user's query and returns
    all results combined into a single block of text.

    Plain explanation:
        Initializes the Tavily client, runs one search per subreddit,
        collects all the text content from every result, and joins it
        together into one big string that Claude can read in the next step.

    Analogy:
        Like a research assistant who visits six different sections of the
        library, photocopies the relevant pages from each section, then
        stacks all the pages into one pile and hands it to you. You get
        everything at once, already collected, ready to read.

    Args:
        user_query: the raw query string the user typed in the frontend

    Returns:
        a single string containing all Reddit content found, or an
        empty string if nothing was found
    """
    # initialize the Tavily client with our API key
    client = TavilyClient(api_key=TAVILY_API_KEY)

    # build our list of subreddit-targeted queries
    queries = build_reddit_queries(user_query)

    all_results = []  # will hold all text content we find across all searches

    for query in queries:
        try:
            # run the search — Tavily returns a dict with a 'results' key
            # each result has 'url', 'title', 'content', and 'score' fields
            response = client.search(
                query=query,               # the search string
                max_results=REDDIT_MAX_RESULTS,  # how many results to fetch
                search_depth="advanced",   # advanced = more thorough search
                include_answer=False,      # we want raw results, not a summary
            )

            # loop through each result Tavily returned
            for result in response.get("results", []):
                # extract the text content of this result
                content = result.get("content", "")
                title   = result.get("title", "")
                url     = result.get("url", "")

                # only include results that actually have content
                if content:
                    # format each result with its title and URL for context
                    # this helps Claude understand where each piece of text came from
                    formatted = f"SOURCE: {title}\nURL: {url}\nCONTENT: {content}"
                    all_results.append(formatted)  # add to our collection

        except Exception as e:
            # if one subreddit search fails, log it and keep going
            # we don't want one failure to kill the whole search
            print(f"Search failed for query '{query}': {e}")
            continue  # move on to the next query

    if not all_results:
        # if we found nothing at all across all subreddits, return empty string
        return ""

    # join all results into one big string separated by dividers
    # this makes it easy for Claude to distinguish between different sources
    combined = "\n\n─────────────────────────────────\n\n".join(all_results)

    return combined  # return the full combined text


# ─────────────────────────────────────────────────────────────────────────────
# Test block — runs only when you execute this file directly
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # a sample query to test with
    test_query = "heat protectants for fine thick hair blow drying"

    print(f"Searching Reddit for: '{test_query}'")
    print("=" * 60)

    # run the search
    results = search_reddit(test_query)

    if results:
        # print just the first 3000 characters so we can see the format
        # without flooding the terminal
        print(results[:3000])
        print("\n... (truncated for display)")
    else:
        print("No results found.")