User query
↓
Tavily → search Reddit (targeted subreddits) → raw posts and comments
↓
Claude → extract product names from Reddit text
↓
For each product:
Tavily → web search for reviews and information
Claude → summarize into pros / cons / best for / price
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
│   ├── product_extractor.py    # Claude: extract product names from Reddit text
│   ├── product_research.py     # Tavily + Claude: research and summarize products
│   ├── config.py               # API keys and constants
│   ├── requirements.txt        # Python dependencies
│   └── .env                    # API keys (never committed to GitHub)
├── frontend/
│   ├── src/
│   │   ├── App.jsx             # Root component, manages state
│   │   ├── components/
│   │   │   ├── SearchBar.jsx   # Query input and submit button
│   │   │   ├── ProductCard.jsx # Individual product result card
│   │   │   └── LoadingState.jsx# Spinner shown while pipeline runs
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

## Future Improvements

- **PRAW integration** — swap Tavily Reddit search for direct Reddit API access
  once approved, enabling precise subreddit targeting and comment threading
- **Caching** — store results for recent queries to avoid redundant API calls
- **User hair profile** — let users save their hair type so queries are
  automatically personalized
- **Product links** — add direct links to Ulta, Sephora, or Amazon for each
  product card
- **Deployment** — host on Railway or Render so friends can access it from
  their phones without running it locally