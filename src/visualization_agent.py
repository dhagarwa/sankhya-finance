import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import List, Dict, Any, Union

class VisualizationAgent:
    def __init__(self):
        self.default_template = "plotly_white"
        self.color_sequence = px.colors.qualitative.Set3

    def create_visualization(self, data: pd.DataFrame, description: str) -> go.Figure:
        """
        Create appropriate visualization based on the data and description.
        
        Args:
            data: DataFrame containing the equity analysis metrics
            description: String describing what to visualize
            
        Returns:
            Plotly figure object
        """
        # Convert description to lowercase for easier matching
        description = description.lower()
        
        if "scatter" in description or "correlation" in description:
            return self._create_scatter_plot(data, description)
        elif "bar" in description or "compare" in description or "comparison" in description:
            return self._create_bar_plot(data, description)
        elif "line" in description or "trend" in description or "time" in description:
            return self._create_line_plot(data, description)
        else:
            return self._create_bar_plot(data, description)  # Default to bar plot

    def _create_scatter_plot(self, data: pd.DataFrame, description: str) -> go.Figure:
        """Create a scatter plot for comparing two metrics."""
        numeric_cols = data.select_dtypes(include=['float64', 'int64']).columns
        
        if len(numeric_cols) < 2:
            raise ValueError("Need at least two numeric columns for scatter plot")
            
        fig = px.scatter(
            data,
            x=numeric_cols[0],
            y=numeric_cols[1],
            color="Ticker" if "Ticker" in data.columns else None,
            hover_data=["Company Name"] if "Company Name" in data.columns else None,
            template=self.default_template,
            title=f"{numeric_cols[1]} vs {numeric_cols[0]}"
        )
        return fig

    def _create_bar_plot(self, data: pd.DataFrame, description: str) -> go.Figure:
        """Create a bar plot for comparing metrics across companies."""
        if "Ticker" not in data.columns:
            raise ValueError("Data must contain 'Ticker' column for bar plot")
            
        numeric_cols = data.select_dtypes(include=['float64', 'int64']).columns
        if len(numeric_cols) < 1:
            raise ValueError("Need at least one numeric column for bar plot")
            
        fig = px.bar(
            data,
            x="Ticker",
            y=numeric_cols[0],
            color="Sector" if "Sector" in data.columns else None,
            hover_data=["Company Name"] if "Company Name" in data.columns else None,
            template=self.default_template,
            title=f"{numeric_cols[0]} by Company"
        )
        return fig

    def _create_line_plot(self, data: pd.DataFrame, description: str) -> go.Figure:
        """Create a line plot for showing trends."""
        if "Ticker" not in data.columns:
            raise ValueError("Data must contain 'Ticker' column for line plot")
            
        numeric_cols = data.select_dtypes(include=['float64', 'int64']).columns
        if len(numeric_cols) < 1:
            raise ValueError("Need at least one numeric column for line plot")
            
        fig = px.line(
            data,
            x="Ticker",
            y=numeric_cols[0],
            color="Sector" if "Sector" in data.columns else None,
            markers=True,
            hover_data=["Company Name"] if "Company Name" in data.columns else None,
            template=self.default_template,
            title=f"{numeric_cols[0]} Trend by Company"
        )
        return fig

    def save_plot(self, fig: go.Figure, filename: str):
        """Save the plot to an HTML file for interactive viewing."""
        fig.write_html(f"{filename}.html")
        
# Example usage
if __name__ == "__main__":
    # Example with data from Yfinance_metrics
    from yfinance_metrics import get_sp500_tickers, fetch_fundamentals
    
    # Get some sample data
    tickers = get_sp500_tickers()[:10]  # Get first 10 tickers
    data = fetch_fundamentals(tickers)
    
    # Create visualization agent
    viz_agent = VisualizationAgent()
    
    # Create different types of plots
    scatter_fig = viz_agent.create_visualization(data, "Create a scatter plot of PE Ratio vs Market Cap")
    viz_agent.save_plot(scatter_fig, "pe_vs_marketcap_scatter")
    
    bar_fig = viz_agent.create_visualization(data, "Compare Market Cap across companies")
    viz_agent.save_plot(bar_fig, "market_cap_comparison")
    
    line_fig = viz_agent.create_visualization(data, "Show trend of Current Price")
    viz_agent.save_plot(line_fig, "price_trend") 