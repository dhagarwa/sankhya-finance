from typing import Dict, List
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
import os

class Step(BaseModel):
    """Schema for each decomposition step"""
    step_number: int = Field(description="The order number of this step")
    description: str = Field(description="What needs to be done")
    required_data: List[str] = Field(description="List of data points needed from YFinance")
    time_period: str = Field(description="Required time range")
    frequency: str = Field(description="Data frequency (daily, quarterly, yearly)")

class QueryDecomposition(BaseModel):
    """Schema for the complete decomposition"""
    query: str = Field(description="Original query")
    steps: List[Step] = Field(description="List of decomposition steps")

class QueryDecomposer:
    """
    A conversational agent that breaks down complex stock-related queries into steps
    using Gemini Flash API via LangChain, with awareness of YFinance data points.
    """
    
    def __init__(self):
        # Initialize the LLM
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash-latest",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0
        )
        
        # Initialize the output parser
        self.parser = JsonOutputParser(pydantic_object=QueryDecomposition)
        
        # Create the prompt template with YFinance data awareness
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a financial query decomposition expert. Break down complex stock-related queries into logical steps.

Available data types from YFinance API:

Company Information:
- Basic Info: Ticker, longName, shortName, industry, sector, website, country
- Business Details: longBusinessSummary, fullTimeEmployees
- Exchange Info: exchange, quoteType, timeZoneFullName, currency

Market Data:
- Price Info: currentPrice, previousClose, open, dayLow, dayHigh, regularMarket* metrics
- Volume: volume, averageVolume, averageVolume10days
- Market Stats: marketCap, impliedSharesOutstanding, sharesOutstanding, floatShares
- Moving Averages: fiftyDayAverage, twoHundredDayAverage
- Trading Range: fiftyTwoWeekLow, fiftyTwoWeekHigh, 52WeekChange

Valuation Metrics:
- PE Ratios: trailingPE, forwardPE, trailingPegRatio
- Price Ratios: priceToBook, priceToSalesTrailing12Months
- Enterprise Values: enterpriseValue, enterpriseToRevenue, enterpriseToEbitda

Financial Performance:
- Margins: profitMargins, grossMargins, operatingMargins, ebitdaMargins
- Returns: returnOnAssets, returnOnEquity
- Growth: earningsGrowth, revenueGrowth, earningsQuarterlyGrowth
- Cash Flow: freeCashflow, operatingCashflow

Balance Sheet:
- Cash & Debt: totalCash, totalCashPerShare, totalDebt
- Ratios: quickRatio, currentRatio, debtToEquity
- Book Value: bookValue, priceToBook

Income Statement:
- Revenue: totalRevenue, revenuePerShare
- Earnings: trailingEps, forwardEps, netIncomeToCommon
- EBITDA: ebitda

Dividends & Splits:
- Dividend Info: dividendRate, dividendYield, payoutRatio
- Historical: fiveYearAvgDividendYield, lastDividendValue, lastDividendDate
- Splits: lastSplitFactor, lastSplitDate

Risk & Governance:
- Risk Metrics: beta, auditRisk, boardRisk, compensationRisk, shareHolderRightsRisk
- Ownership: heldPercentInsiders, heldPercentInstitutions
- Short Interest: sharesShort, shortRatio, shortPercentOfFloat

Analyst Coverage:
- Recommendations: recommendationMean, recommendationKey, numberOfAnalystOpinions
- Price Targets: targetHighPrice, targetLowPrice, targetMeanPrice, targetMedianPrice

When breaking down queries:
1. Identify required data points from the above categories
2. Specify time periods needed (e.g., last quarter, TTM, 5 years)
3. Define the frequency of data needed (daily, quarterly, yearly)
4. Consider any calculations or comparisons needed
5. if the data is retrievd already, do not retrieve it again and use the data to do the next steps to answer the query of the user

{format_instructions}"""),
            ("user", "{query}")
        ])

    async def decompose_query(self, query: str) -> Dict:
        """Decompose a natural language query into structured steps."""
        try:
            # Create the chain
            chain = self.prompt | self.llm | self.parser
            
            # Run the chain
            result = await chain.ainvoke({
                "query": query,
                "format_instructions": self.parser.get_format_instructions()
            })
            
            return result
            
        except Exception as e:
            print(f"Error decomposing query: {str(e)}")
            return None 