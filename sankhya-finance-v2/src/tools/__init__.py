"""
Tools - External capabilities that graph nodes can invoke.

Tools are decorated with @tool from langchain_core and can be called
by the StepExecutorNode during DATA step execution.

Tool overview:
    - yfinance_tools:    Yahoo Finance API wrappers (income statements, prices, metrics,
                         analyst recommendations, institutional holders, options)
    - web_search:        Web search and news search via DuckDuckGo (no API key needed)
    - sec_edgar_tools:   SEC EDGAR API for filings, XBRL financial data, and insider trades
                         (fully free, no API key required)
    - fred_tools:        Federal Reserve (FRED) API for macroeconomic indicators --
                         interest rates, GDP, inflation, unemployment, treasury yields
                         (free API key required)
    - fmp_tools:         Financial Modeling Prep API for analyst estimates, company ratings,
                         and earnings surprises (free tier: 250 calls/day)
    - ticker_extractor:  LLM-powered natural language to S&P 500 ticker translation

All tools are registered in yfinance_tools.TOOLS_BY_NAME and TOOL_REGISTRY,
which serve as the single lookup point for the StepExecutor and Decomposer.
"""
