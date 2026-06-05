# app.py
# ─────────────────────────────────────────────────────────────────────────────
# Flask API server for the Haircare Advisor.
# Receives queries from the React frontend, runs the full pipeline,
# and returns structured product results as JSON.
#
# Plain explanation:
#   This script is the entry point for the backend. It creates one API
#   endpoint that the React frontend calls. When a query comes in, it
#   runs all three pipeline steps in sequence — Reddit search, product
#   extraction, product research — and returns the results as JSON.
#
# Analogy:
#   Think of this as the manager of a restaurant kitchen. The frontend
#   is the waiter who takes the customer's order (the query) and brings
#   it to the manager. The manager delegates to the kitchen staff
#   (reddit_search, product_extractor, product_research), collects the
#   finished dishes, and hands them back to the waiter to serve.
# ─────────────────────────────────────────────────────────────────────────────

from flask import Flask, request, jsonify  # Flask core — app, request handling, JSON responses
from flask_cors import CORS                # allows React frontend to call this API
from config import FLASK_PORT, FLASK_DEBUG # our port and debug settings
from reddit_search import search_reddit    # Step 1: search Reddit
from product_extractor import extract_products  # Step 2: extract product names
from product_research import research_all_products  # Step 3: research each product

# ── Initialize Flask app ──────────────────────────────────────────────────────
app = Flask(__name__)  # create the Flask application instance

# enable CORS for all routes so React (running on port 5173) can call this API
# without CORS, browsers block cross-origin requests for security reasons
CORS(app)


# ── Health check endpoint ─────────────────────────────────────────────────────
@app.route("/health", methods=["GET"])
def health():
    """
    Simple health check endpoint.

    Plain explanation:
        Returns a simple JSON response confirming the server is running.
        Useful for quickly verifying the backend is up before the frontend
        tries to use it.

    Analogy:
        Like knocking on the kitchen door and asking "is anyone in there?"
        before placing a big order. Just a quick confirmation things are live.
    """
    return jsonify({"status": "ok", "message": "Haircare Advisor API is running"})


# ── Main search endpoint ──────────────────────────────────────────────────────
@app.route("/search", methods=["POST"])
def search():
    """
    Main pipeline endpoint — takes a query and returns product recommendations.

    Plain explanation:
        Receives a POST request from the React frontend containing the user's
        query string. Runs all three pipeline steps in sequence and returns
        a JSON response with the results, or an error if something goes wrong.

    Analogy:
        The manager receives the order slip from the waiter, delegates each
        course to the appropriate kitchen station, waits for everything to
        be plated, then hands the complete meal back to the waiter. If
        anything goes wrong in the kitchen, the manager sends back a
        clear error message rather than a half-finished plate.

    Request body (JSON):
        {"query": "heat protectants for fine thick hair"}

    Response body (JSON):
        {
            "query": "heat protectants for fine thick hair",
            "products": [...],
            "total": 6
        }
    """
    # ── Parse the incoming request ────────────────────────────────────────────
    data = request.get_json()  # parse the JSON body of the POST request

    # make sure a query was actually provided
    if not data or "query" not in data:
        # return a 400 Bad Request error if the query is missing
        return jsonify({"error": "Missing 'query' field in request body"}), 400

    query = data["query"].strip()  # get the query string and remove whitespace

    # reject empty queries
    if not query:
        return jsonify({"error": "Query cannot be empty"}), 400

    print(f"\n{'='*60}")
    print(f"New search request: '{query}'")
    print(f"{'='*60}")

    # ── Step 1: Search Reddit ─────────────────────────────────────────────────
    print("Step 1: Searching Reddit...")
    reddit_text = search_reddit(query)  # returns raw Reddit content as string

    # if Reddit search returned nothing, tell the frontend
    if not reddit_text:
        return jsonify({
            "query": query,
            "products": [],
            "total": 0,
            "message": "No Reddit discussions found for this query. Try a more specific search."
        })

    print(f"Found {len(reddit_text)} characters of Reddit content")

    # ── Step 2: Extract product names ─────────────────────────────────────────
    print("Step 2: Extracting product names...")
    products = extract_products(reddit_text, query)  # returns list of dicts

    # if no products were found, tell the frontend
    if not products:
        return jsonify({
            "query": query,
            "products": [],
            "total": 0,
            "message": "No specific products found in Reddit discussions. Try rephrasing your query."
        })

    print(f"Found {len(products)} products")

    # ── Step 3: Research each product ─────────────────────────────────────────
    print("Step 3: Researching products...")
    summaries = research_all_products(products)  # returns list of full summary dicts

    print(f"Research complete — returning {len(summaries)} products")

    # ── Return results to frontend ────────────────────────────────────────────
    return jsonify({
        "query": query,           # echo the original query back
        "products": summaries,    # the full list of product summaries
        "total": len(summaries)   # how many products were found
    })


# ── Run the server ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"Starting Haircare Advisor API on port {FLASK_PORT}...")
    app.run(
        host="0.0.0.0",       # accept connections from any network interface
        port=FLASK_PORT,       # use the port defined in config.py
        debug=FLASK_DEBUG      # enable auto-reload on code changes
    )