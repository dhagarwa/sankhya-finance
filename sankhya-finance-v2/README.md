# Sankhya Finance v2

**LangGraph-powered equity analysis agent with multi-source financial data.**

An AI agent that takes natural language questions about stocks and companies, decomposes them into executable steps, fetches data from 5 different sources (21 tools), verifies quality at each step, and produces structured analysis with React component output.

---

## Architecture

```
                            ┌─────────────────────────────────────────┐
                            │           USER QUERY                     │
                            │  "Is NVIDIA a good investment right now?" │
                            └────────────────┬────────────────────────┘
                                             │
                                             ▼
                            ┌─────────────────────────────┐
                            │       QUERY ROUTER           │
                            │  LLM classifies:             │
                            │  financial → Decomposer      │
                            │  non-financial → Direct       │
                            └──────┬──────────────┬────────┘
                                   │              │
                            financial        non-financial
                                   │              │
                                   ▼              ▼
                     ┌──────────────────┐  ┌──────────────────┐
                     │   DECOMPOSER     │  │ DIRECT RESPONSE  │
                     │                  │  │ Answers from      │
                     │ 1. Extract       │  │ general knowledge │
                     │    tickers       │  └────────┬─────────┘
                     │ 2. Plan steps:   │           │
                     │    DATA → fetch  │           │
                     │    ANALYSIS →    │           │
                     │    reason        │           │
                     └────────┬─────────┘           │
                              │                     │
                    ┌─────────▼──────────┐          │
                    │   STEP EXECUTOR    │◄──┐      │
                    │                    │   │      │
                    │ Calls tools:       │   │      │
                    │ • YFinance (11)    │   │      │
                    │ • SEC EDGAR (3)    │   │      │
                    │ • FRED (2)         │   │      │
                    │ • FMP (3)          │   │      │
                    │ • Web Search (2)   │   │      │
                    └────────┬───────────┘   │      │
                             │               │      │
                    ┌────────▼───────────┐   │      │
                    │     VERIFIER       │   │      │
                    │                    │   │      │
                    │ LLM checks:       │   │      │
                    │ • Completeness    │   │      │
                    │ • Correctness     │   │      │
                    │ • Relevance to    │   │      │
                    │   ORIGINAL QUERY  │   │      │
                    │                    │   │      │
                    │ Verdicts:          │   │      │
                    │ OK → next step     │   │      │
                    │ NEEDS_MORE_DATA ───┘   │      │
                    │ REPLAN → Decomposer   │      │
                    └────────┬───────────┘   │      │
                             │               │      │
                      (all steps done)       │      │
                             │               │      │
                    ┌────────▼───────────────┐      │
                    │   OUTPUT FORMATTER     │◄─────┘
                    │                        │
                    │ Produces:              │
                    │ • Structured JSON      │
                    │ • React/TypeScript     │
                    │   component            │
                    │ • Key insights         │
                    │ • Recommendations      │
                    └────────┬───────────────┘
                             │
                             ▼
                    ┌─────────────────────┐
                    │    FINAL OUTPUT     │
                    └─────────────────────┘
```

---

## Journey of a Query

Here is the complete lifecycle of a query through the system, using a real example:

### Query: *"Analyze NVIDIA's revenue growth and compare it with AMD"*

**Step 1 — Query Router** (`src/nodes/query_router.py`)
```
Input:  "Analyze NVIDIA's revenue growth and compare it with AMD"
Action: LLM classifies as FINANCIAL (needs real data, not just general knowledge)
Output: query_type = "financial" → routes to Decomposer
```

**Step 2 — Ticker Extraction** (`src/tools/ticker_extractor.py`)
```
Action: LLM analyzes query → searches 504-company S&P 500 database
Output: detected_tickers = ["NVDA", "AMD"]
```

**Step 3 — Decomposer** (`src/nodes/decomposer.py`)
```
Action: LLM sees 21 available tools, creates an execution plan:

  step_1 (DATA):     get_income_statements(ticker="NVDA", period="annual", limit=5)
  step_2 (DATA):     get_income_statements(ticker="AMD", period="annual", limit=5)
  step_3 (DATA):     get_key_metrics(ticker="NVDA")
  step_4 (DATA):     get_key_metrics(ticker="AMD")
  step_5 (ANALYSIS): "Compare NVDA and AMD revenue growth using step_1-4 data"

Each step knows its dependencies (step_5 depends on steps 1-4).
```

**Step 4 — Execute + Verify Loop** (`src/nodes/step_executor.py` + `src/nodes/verifier.py`)
```
For each step:
  1. Executor calls the tool (or LLM for ANALYSIS steps)
  2. Verifier checks the result against the ORIGINAL query:
     - Is the data complete? Are the numbers reasonable?
     - Does this actually help answer what the user asked?
  3. Verdict:
     - OK → move to next step
     - NEEDS_MORE_DATA → retry with adjusted parameters (max 2 retries)
     - REPLAN → scrap the plan, go back to Decomposer (max 1 replan)
```

**Step 5 — Output Formatter** (`src/nodes/output_formatter.py`)
```
Action: Combines all step results into:
  1. Structured JSON with summary, content blocks (metrics, tables, charts),
     key insights, and recommendations
  2. React/TypeScript component code for frontend rendering
```

---

## Project Structure

```
sankhya-finance-v2/
│
├── src/
│   ├── graph.py                 # LangGraph StateGraph definition (7 nodes, edges, routing)
│   ├── state.py                 # FinanceState TypedDict + Pydantic models
│   ├── main.py                  # CLI entry point (interactive + single query + debug)
│   │
│   ├── nodes/                   # Graph nodes (each is an async function)
│   │   ├── query_router.py      # Classifies queries as financial vs non-financial
│   │   ├── direct_response.py   # Handles non-financial queries
│   │   ├── decomposer.py       # Plans multi-step execution from natural language
│   │   ├── step_executor.py    # Executes DATA/ANALYSIS steps
│   │   ├── verifier.py         # LLM quality check after every step
│   │   └── output_formatter.py # Produces structured JSON + TypeScript output
│   │
│   ├── tools/                   # External data capabilities (21 tools)
│   │   ├── yfinance_tools.py   # Yahoo Finance: 11 tools (price, statements, metrics, options...)
│   │   ├── sec_edgar_tools.py  # SEC EDGAR: 3 tools (filings, XBRL financials, insider trades)
│   │   ├── fred_tools.py       # Federal Reserve: 2 tools (economic indicators, yield curve)
│   │   ├── fmp_tools.py        # Financial Modeling Prep: 3 tools (estimates, ratings, earnings)
│   │   ├── web_search.py       # DuckDuckGo: 2 tools (web search, news search)
│   │   └── ticker_extractor.py # LLM-powered natural language → ticker translation
│   │
│   ├── data/
│   │   └── sp500_companies.py  # 504 S&P 500 companies with sector/industry/keywords
│   │
│   └── utils/
│       └── model_config.py     # Single-point LLM configuration (model, temperature, tokens)
│
├── tests/
│   ├── query_generator.py       # 16 query templates across 8 equity analysis categories
│   ├── test_data_tools.py       # Tool-level tests (free, no LLM, fast)
│   ├── test_full_pipeline.py    # Full graph pipeline tests (with LLM, debug logging)
│   └── results/                 # Test output (JSONL logs, summaries)
│
├── .env.template                # Environment variable template
└── requirements.txt             # Python dependencies
```

---

## Data Sources (21 Tools)

### Free, No API Key Required

| Source | Tools | What It Provides |
|--------|-------|-----------------|
| **Yahoo Finance** | 11 tools | Stock prices, financial statements (income/balance/cash flow), key metrics (P/E, margins, ROE), analyst recommendations, institutional holders, options data, company info, news |
| **SEC EDGAR** | 3 tools | Official SEC filings (10-K, 10-Q, 8-K), XBRL-structured financial data directly from filings (supports both US-GAAP and IFRS filers), insider transactions (Form 4) |
| **DuckDuckGo** | 2 tools | General web search, news-specific search |

### Free Tier, API Key Required

| Source | Tools | What It Provides | Get Key |
|--------|-------|-----------------|---------|
| **FRED** (Federal Reserve) | 2 tools | 28+ macro indicators (GDP, CPI, unemployment, fed funds rate, treasury yields with inversion detection) | [fred.stlouisfed.org](https://fred.stlouisfed.org/docs/api/api_key.html) |
| **Financial Modeling Prep** | 3 tools | Analyst consensus estimates (forward EPS/revenue), company financial health ratings (S-F scale), earnings surprises (beat/miss history) | [financialmodelingprep.com](https://financialmodelingprep.com/developer/docs/) |

All tools return a **consistent JSON schema** regardless of ticker. When a tool can't fetch data (bad ticker, missing API key, rate limit), it returns `{"error": "descriptive message"}` instead of crashing.

---

## State Management

The entire graph shares a single `FinanceState` TypedDict. Every node reads from it and returns a partial update. LangGraph merges updates automatically.

```python
class FinanceState(TypedDict, total=False):
    # Input
    query: str                              # Original user question

    # Router
    query_type: QueryType                   # FINANCIAL | NON_FINANCIAL

    # Decomposer
    steps: list[DecompositionStep]          # Execution plan
    detected_tickers: list[str]             # Extracted ticker symbols

    # Executor
    current_step_index: int                 # Which step we're on
    step_results: dict[str, StepResult]     # Results keyed by step_id

    # Verifier
    verification: VerificationResult        # OK | NEEDS_MORE_DATA | REPLAN
    retry_count: int                        # Per-step retry counter
    replan_count: int                       # Plan-level replan counter

    # Output
    structured_output: dict[str, Any]       # Frontend-ready JSON
    typescript_component: dict[str, Any]    # React component code
```

Key Pydantic models enforce structure:
- **`DecompositionStep`** — step_id, type (DATA/ANALYSIS), tool_name, parameters, dependencies
- **`StepResult`** — success/failure, data dict (for DATA steps) or analysis text (for ANALYSIS steps)
- **`VerificationResult`** — verdict, explanation, optional retry_step or replan_reason

---

## Self-Correction Mechanisms

The system has three layers of error recovery:

| Mechanism | Trigger | Action | Limit |
|-----------|---------|--------|-------|
| **Retry** | Verifier says `NEEDS_MORE_DATA` | Re-execute current step with modified parameters | 2 per step |
| **Replan** | Verifier says `REPLAN` | Go back to Decomposer, create entirely new plan | 1 per query |
| **Recursion limit** | Graph exceeds 40 node calls | Force-stop and output whatever data we have | Hard limit |

The Verifier always checks results against the **original user query** (stored in `state["query"]`), not just the step description. This ensures the system stays aligned with user intent throughout multi-step execution.

---

## Setup

```bash
# 1. Clone
git clone https://github.com/dhagarwa/sankhya-finance.git
cd sankhya-finance/sankhya-finance-v2

# 2. Create environment
conda create -n sankhya-v2-env python=3.11 -y
conda activate sankhya-v2-env
pip install -r requirements.txt

# 3. Configure API keys
cp .env.template .env
# Edit .env: add your OPENAI_API_KEY (required)
# Optionally add FRED_API_KEY and FMP_API_KEY for richer analysis

# 4. Run
python -m src.main                          # Interactive mode
python -m src.main -q "What is AAPL's P/E?" # Single query
python -m src.main -d                       # Debug mode
```

---

## Testing

### Layer 1: Data Tools (free, fast, no LLM)

Tests each of the 21 tools against S&P 500 tickers to verify schema consistency.

```bash
# Quick: 13 free tools x 10 tickers
python -m tests.test_data_tools --count 10 --free-only --fast-only

# All free tools, all 504 tickers
python -m tests.test_data_tools --all --free-only

# Specific tool or ticker
python -m tests.test_data_tools --tool get_sec_financial_data --all
python -m tests.test_data_tools --ticker TSLA
```

### Layer 2: Full Pipeline (LLM-powered, debug logging)

Runs queries through the complete graph and logs every node decision.

```bash
# Single ticker with full debug trace
python -m tests.test_full_pipeline --ticker AAPL

# Batch test
python -m tests.test_full_pipeline --count 20

# Resume from previous run
python -m tests.test_full_pipeline --count 50 --resume

# Test a sector
python -m tests.test_full_pipeline --sector "Financials" --all

# Custom query
python -m tests.test_full_pipeline --ticker TSLA --query "Is Tesla overvalued?"
```

Results are saved to `tests/results/` as JSONL (one JSON per line) for analysis.

---

## Design Decisions

**Why LangGraph over raw LangChain agents?**
State management. Financial analysis queries involve multiple data fetches with dependencies between them. LangGraph's typed state + conditional edges make the decompose-execute-verify loop clean and debuggable. Raw agents would need prompt-hacking to achieve the same control flow.

**Why 5 data sources instead of just YFinance?**
YFinance is great for a quick snapshot, but equity analysis needs depth: SEC XBRL data for authoritative multi-year fundamentals, FRED for macro context (interest rates drive valuations), FMP for forward-looking analyst estimates (trailing P/E is useless without forward P/E), and SEC insider trades as a sentiment signal.

**Why verify every step with an LLM?**
Financial data APIs are unreliable — they return nulls, stale data, wrong tickers, or partial results silently. The Verifier catches these before they cascade into bad analysis. It also checks relevance against the original query, preventing plan drift in multi-step execution.

**Why generate TypeScript components?**
The agent is designed to power a frontend. Structured JSON is for data; the TypeScript component is a complete, self-contained React widget that renders the analysis with charts (Recharts), tables, and metrics — ready to drop into a Next.js app.

---

## Cost Estimates

| Operation | LLM Calls | Approximate Cost |
|-----------|-----------|-----------------|
| Simple query (price, single metric) | ~5 calls | ~$0.02-0.05 |
| Moderate query (fundamentals + analysis) | ~8 calls | ~$0.05-0.15 |
| Complex query (multi-company comparison) | ~12-15 calls | ~$0.10-0.30 |
| Full test suite (504 companies) | ~3000 calls | ~$15-75 |

Using `gpt-4o` as the default model. Costs can be reduced by switching to `gpt-4o-mini` for simpler nodes (router, ticker extraction) via `model_config.py`.
