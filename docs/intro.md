# Haircare Advisor

A full-stack AI-powered web application that helps users find haircare product
recommendations by mining real community discussions on Reddit and synthesizing
them into structured, comparable product cards.

---

## What This Project Is

Finding the right haircare products is genuinely hard. The best advice lives in
Reddit communities — real people with your exact hair type explaining exactly
why a product worked or didn't. But surfacing that advice requires manually
searching Reddit, reading dozens of threads, cross-referencing products on
Ulta, Amazon, and Sephora, and synthesizing it all yourself.

Haircare Advisor automates that entire workflow. You type a natural language
query — "heat protectants for fine thick hair for blow drying" or "I have
curly hair, what products should I use?" — and the app searches Reddit, extracts
product recommendations, researches each product across the web, and returns
clean product cards with pros, cons, best-for notes, and price ranges.

---

## What You'll Learn

- **Full-stack AI application architecture** — how a React frontend, Flask API
  backend, and multiple external AI services fit together into one cohesive app
- **LLM chaining** — using Claude twice in sequence: once to extract structured
  data from messy text, once to synthesize research into a readable summary
- **Parallel execution** — using Python's ThreadPoolExecutor to research
  multiple products simultaneously, cutting response time by ~3x
- **Search API integration** — using Tavily to perform intelligent web searches
  and Reddit-targeted searches programmatically
- **Prompt engineering** — writing precise prompts that instruct Claude to return
  structured JSON output reliably
- **React + Vite frontend** — building a polished, component-based UI
- **Flask as a pure API** — serving JSON responses instead of HTML templates,
  designed to work with a separate frontend
- **CORS** — understanding why browsers block cross-origin requests and how to
  configure Flask to allow them
- **Environment management** — keeping API keys secure with .env files and
  python-dotenv
- **Error handling in pipelines** — gracefully managing failures at any step in
  a multi-service chain

---

## Tech Stack

### Backend
| Tool | Purpose |
|---|---|
| Python 3 | Core backend language |
| Flask | Web framework — serves the API |
| flask-cors | Allows React frontend to talk to Flask |
| python-dotenv | Loads API keys from .env file |

### Frontend
| Tool | Purpose |
|---|---|
| React | Component-based UI framework |
| Vite | Fast development server and build tool |

### APIs & Services
| Service | Purpose |
|---|---|
| Tavily | Searches Reddit and the broader web for product information |
| Anthropic Claude (claude-sonnet-4-5) | Extracts product names from Reddit text; summarizes product research |

---

## The AI Component

This app uses Claude in two distinct ways within the same pipeline:

**Step 1 — Information Extraction**
After Tavily retrieves raw Reddit posts and comments, Claude reads that messy,
unstructured community discussion and extracts a clean list of specific product
names along with community sentiment — positive (recommended) or negative
(warned against). This is a classic NLP extraction task — turning noise into
signal.

**Step 2 — Research Synthesis**
For each extracted product, Tavily searches the web for reviews and information.
Claude then reads those search results and synthesizes them into structured
output: pros, cons, who the product is best for, approximate price, and a
one-sentence verdict. This is a summarization and reasoning task — condensing
many sources into one coherent, useful summary.

The two Claude calls are chained together: the output of the first (product
names with sentiment) becomes the input driver for the second (per-product
research). Products are researched in parallel using ThreadPoolExecutor,
cutting total response time from ~60 seconds to ~20 seconds.

---

## The Pipeline
User query
↓
Tavily → search Reddit (targeted subreddits) → raw posts and comments
↓
Claude → extract product names with sentiment (positive/negative)
↓
For each product (run in parallel via ThreadPoolExecutor):
Tavily → web search for reviews and information
Claude → summarize into pros / cons / best for / price / verdict
↓
Flask → return structured JSON to frontend
↓
React → display product cards in browser

---

## Project Structure

haircare_advisor/
├── backend/
│   ├── app.py                  # Flask API — routes and orchestration
│   ├── reddit_search.py        # Tavily: search Reddit content
│   ├── product_extractor.py    # Claude: extract product names with sentiment
│   ├── product_research.py     # Tavily + Claude: research products in parallel
│   ├── config.py               # API keys and constants
│   ├── requirements.txt        # Python dependencies
│   └── .env                    # API keys (never committed to GitHub)
├── frontend/
│   ├── src/
│   │   ├── App.jsx             # Root component, manages state
│   │   ├── components/
│   │   │   ├── SearchBar.jsx   # Query input and submit button
│   │   │   ├── ProductCard.jsx # Individual product result card
│   │   │   ├── LoadingState.jsx# Spinner shown while pipeline runs
│   │   │   └── ActivityFeed.jsx# Live pipeline status panel
│   │   └── index.css           # Global styles
│   ├── package.json
│   └── vite.config.js
├── .gitignore
└── README.md

---

## API Keys Required

| Service | Where to get it | Cost |
|---|---|---|
| Anthropic | console.anthropic.com | ~$0.05–$0.10 per query |
| Tavily | tavily.com | Free tier: 1,000 searches/month |

---

## Running Locally

**Terminal 1 — Backend:**
```bash
cd backend
source venv/bin/activate
python3 app.py
```

**Terminal 2 — Frontend:**
```bash
cd frontend
nvm use 22
npm run dev
```

Then open http://localhost:5173 in your browser.

---

## Future Improvements

- **PRAW integration** — swap Tavily Reddit search for direct Reddit API access
  once approved, enabling precise subreddit targeting and comment threading
- **Caching** — store results for recent queries to avoid redundant API calls
- **Product links** — add direct links to Ulta, Sephora, or Amazon for each
  product card
- **Deployment** — host on Railway or Render so friends can access it from
  their phones without running it locally
- **Hair profile** — let users save their hair type so queries are
  automatically personalized