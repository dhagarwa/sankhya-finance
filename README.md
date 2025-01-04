# sankhya-finance
A smart toolkit for financial stock analysis. No convoluted data, the right data visualized the right way 

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 16+
- API keys for:
  - Polygon.io (stock data)
  - Google AI (Gemini model)

### Environment Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/sankhya-finance.git
   cd sankhya-finance
   ```

2. Set up the Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Install Node.js dependencies:
   ```bash
   cd src
   npm install
   ```

4. Create a `.env` file in the root directory similar to `.env.template`:
   ```
   POLYGON_API_KEY=your_polygon_api_key
   GOOGLE_AI_API_KEY=your_google_ai_api_key
   ```

5. Start the development servers:
   
   Backend:
   ```bash
   # In the root directory in the visualization/server directory
   python app.py
   ```

   Frontend:
   ```bash
   # In the src/agents/website directory
   npm run dev
   ```

6. Open your browser and navigate to `http://localhost:4321`

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

