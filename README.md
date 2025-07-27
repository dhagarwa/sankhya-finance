# Sankhya Finance

> AI-Powered Financial Analysis with OpenAI O3 Reasoning

A modern financial analysis toolkit that uses **OpenAI's O3 reasoning model** to intelligently decompose complex financial queries and retrieve data through **Yahoo Finance**.

## 🎯 What Makes This Special

- **🧠 O3 Reasoning**: Uses OpenAI's advanced reasoning model to break down complex financial questions into executable steps
- **🔄 Iterative Analysis**: The AI can see partial results and adjust its analysis strategy dynamically  
- **📊 Free Financial Data**: Leverages Yahoo Finance for comprehensive, free financial data access
- **🤖 Natural Language**: Ask questions in plain English - no need to learn complex APIs

## 🚀 Features

### AI-Powered Query Decomposition
```
Query: "Compare Apple and Microsoft revenue growth over the last 4 quarters"

O3 Reasoning Output:
Step 1: Get AAPL income statements (quarterly, last 4 periods)
Step 2: Get MSFT income statements (quarterly, last 4 periods)  
Step 3: Calculate revenue growth rates for both companies
Step 4: Generate comparative analysis with insights
```

### Supported Financial Data
- **Income Statements** (annual/quarterly)
- **Balance Sheets** (annual/quarterly)
- **Cash Flow Statements** (annual/quarterly)
- **Stock Prices** (current/historical)
- **Company News** and market updates
- **Crypto Data** (prices, historical trends)

### Example Queries
- *"What is Tesla's current stock price and recent news?"*
- *"Show me Netflix's cash flow trends over the last 5 years"*
- *"Compare Amazon and Google's profit margins"*
- *"Get balance sheet data for the top 3 tech stocks"*

## 📦 Installation

### Prerequisites
- Python 3.10+
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys)) - Optional, system works without it using YFinance directly

### Setup
```bash
# 1. Clone the repository
git clone https://github.com/yourusername/sankhya-finance.git
cd sankhya-finance

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp env.example .env
# Edit .env with your API keys

# 5. Run the system
python src/main.py
```

## 🎮 Usage

### Interactive Mode
```bash
python src/main.py
# Select option 1 for interactive query mode
```

### Test Queries
```bash
python src/main.py
# Select option 2 to run predefined test queries
```

### Example Session
```
🚀 SANKHYA FINANCE - AI Financial Analysis
Query: What is Apple's current stock price?
================================================================================

📊 Step 1: Query Pattern Analysis
   Query Type: current_data
   Detected Tickers: ['AAPL']

🧠 Step 2: O3 Reasoning & MCP Execution
🧠 O3 Reasoning: Starting query decomposition...
🔧 Executing step_1: Get current stock price for AAPL
✅ step_1 completed successfully

📈 Step 3: Analysis Results
--------------------------------------------------
✅ Successful Steps: 1
❌ Failed Steps: 0

🎯 Final Analysis:
--------------------------------------------------
Apple Inc. (AAPL) is currently trading at $195.42 per share...
```

## 🛠️ Architecture

### Modern AI-First Design
```
User Query
    ↓
[O3 Reasoning Model] ← Iterative refinement
    ↓
[Query Decomposition] ← Step-by-step planning  
    ↓
[YFinance Client] ← Yahoo Finance API (Free!)
    ↓
[Results Analysis] ← O3 generates insights
    ↓
Human-readable Answer
```

### Key Components

1. **O3QueryDecomposer** (`src/agents/o3_query_decomposer.py`)
   - Uses OpenAI's O3 model for intelligent query breakdown
   - Iteratively refines execution plan based on available data
   - Generates comprehensive final analysis

2. **YFinance Client** (`src/agents/yfinance_client.py`)  
   - Direct interface with Yahoo Finance
   - Handles all financial data retrieval (free!)
   - Robust error handling and response formatting

3. **Main Controller** (`src/main.py`)
   - Orchestrates the entire analysis pipeline
   - Provides interactive and batch processing modes
   - User-friendly interface with rich formatting

## 🔧 Configuration

### Environment Variables
```bash
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional  
DEBUG=false
```

### Three-Step Processing Pipeline
1. **DATA RETRIEVAL**: YFinance tools collect raw financial data
2. **ANALYSIS**: GPT-4o processes and calculates insights
3. **OUTPUT**: Results are formatted and displayed clearly

### Available YFinance Tools
The system automatically has access to these financial data tools:
- `get_income_statements` - Company income statements
- `get_balance_sheets` - Company balance sheets  
- `get_cash_flow_statements` - Company cash flow data
- `get_current_stock_price` - Real-time stock prices
- `get_historical_stock_prices` - Historical price data
- `get_company_news` - Latest company news
- `get_company_info` - Basic company information

## 🎯 Use Cases

### For Investors
- Quick fundamental analysis of stocks
- Competitive comparison between companies
- Historical trend analysis
- News sentiment tracking

### For Analysts  
- Automated data collection for reports
- Multi-company comparative studies
- Time-series analysis of key metrics
- Due diligence research

### For Developers
- Financial data integration for apps
- AI-powered investment tools  
- Automated trading research
- Financial dashboard backends

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup
```bash
# Install development dependencies
pip install -r requirements.txt

# Run tests
pytest

# Format code
black src/

# Type checking
mypy src/
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Yahoo Finance](https://finance.yahoo.com/) for providing free, comprehensive financial data
- [YFinance Python Library](https://pypi.org/project/yfinance/) for easy Yahoo Finance API access
- [OpenAI](https://openai.com/) for the powerful GPT-4o reasoning model

## 🔗 Related Projects

- [YFinance Library](https://pypi.org/project/yfinance/) - The Python library powering our financial data access
- [OpenAI Models](https://platform.openai.com/docs/models) - Documentation for GPT-4o and other models

---

**Built with ❤️ for the financial analysis community**
