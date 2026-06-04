# config.py
# ─────────────────────────────────────────────────────────────────────────────
# Central configuration for the Haircare Advisor backend.
#
# Plain explanation:
#   This file loads all API keys from the .env file and defines constants
#   that the rest of the app uses. Every other script imports from here
#   instead of hardcoding values directly.
#
# Analogy:
#   Think of this as the control panel for the whole app. Instead of every
#   room in a building having its own thermostat, there's one central panel
#   that everything reads from. Change a value here and it changes everywhere.
# ─────────────────────────────────────────────────────────────────────────────

import os                      # lets us read environment variables from the system
from dotenv import load_dotenv # loads variables from our .env file into the environment

# Load the .env file so all our API keys become available as environment variables
load_dotenv()

# ── API Keys ──────────────────────────────────────────────────────────────────
# os.getenv() reads the value of an environment variable by name
# If the variable isn't found, it returns None
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
TAVILY_API_KEY    = os.getenv("TAVILY_API_KEY")

# ── Claude Model ──────────────────────────────────────────────────────────────
# The specific Claude model we'll use for all LLM calls in this app
# claude-sonnet-4-20250514 is the current Claude Sonnet 4 model string
CLAUDE_MODEL = "claude-sonnet-4-5"

# ── Reddit Search Settings ────────────────────────────────────────────────────
# How many Tavily search results to retrieve when searching Reddit
REDDIT_MAX_RESULTS = 10

# The subreddits we want to focus our search on
# Tavily will use these to construct targeted site:reddit.com queries
TARGET_SUBREDDITS = [
    "femalehairadvice",
    "curlyhair",
    "HaircareScience",
    "Hair",
    "beauty",
    "SkincareAddiction",
]

# ── Product Research Settings ─────────────────────────────────────────────────
# Maximum number of products to research after extracting from Reddit
# Keeping this low controls cost — each product = one Tavily search + one Claude call
MAX_PRODUCTS_TO_RESEARCH = 6

# How many Tavily search results to retrieve per product during research
PRODUCT_SEARCH_RESULTS = 5

# ── Flask Settings ────────────────────────────────────────────────────────────
# The port Flask will run on locally
FLASK_PORT = 5008

# Whether Flask runs in debug mode (True = auto-reloads on code changes)
# Always set to False in production
FLASK_DEBUG = True