import pandas as pd
import asyncio
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from bucket_fundamentals import analyze_saas_companies
from bucket_fundamentals import fetch_saas_trifecta_history, create_saas_trifecta_index



from bucket_fundamentals import fetch_saas_trifecta_history, create_saas_trifecta_index
import pandas as pd
import asyncio
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

def calculate_index_returns(index_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate cumulative returns for the weighted price index.
    Takes the first quarter as baseline (0%) and calculates returns from there.
    
    Args:
        index_df: DataFrame containing the weighted price index data
    
    Returns:
        DataFrame with added cumulative return column
    """
    # Make a copy to avoid modifying original
    df = index_df.copy()
    
    # Get baseline price (first quarter)
    baseline_price = df['weighted_price'].iloc[0]
    
    # Calculate cumulative returns as percentage from baseline
    df['cumulative_return'] = ((df['weighted_price'] / baseline_price) - 1) * 100
    
    # Round to 2 decimal places
    df['cumulative_return'] = df['cumulative_return'].round(2)
    
    return df

def plot_index_performance(index_df: pd.DataFrame, output_dir: str = 'exports') -> None:
    """
    Create plots for SaaS Trifecta index performance
    """
    plt.style.use('seaborn-v0_8')
    
    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 12))
    
    # Plot 1: Cumulative Returns
    sns.lineplot(data=index_df, x='quarter', y='cumulative_return', 
                marker='o', linewidth=2, markersize=8, ax=ax1)
    ax1.set_title('SaaS Trifecta Index Cumulative Returns (%)', fontsize=12)
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45)
    ax1.axhline(y=0, color='r', linestyle='--', alpha=0.3)
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Company Weights Over Time
    weight_cols = [col for col in index_df.columns if col.endswith('_weight')]
    weights_data = index_df[['quarter'] + weight_cols]
    
    # Create stacked bar plot for weights
    weights_data.plot(x='quarter', y=weight_cols, kind='bar', stacked=True, 
                     ax=ax2, width=0.8)
    ax2.set_title('SaaS Trifecta Components Weights (%)', fontsize=12)
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45)
    ax2.grid(True, alpha=0.3)
    ax2.legend(title='Company Weights', bbox_to_anchor=(1.05, 1))
    
    plt.tight_layout()
    
    # Save plots
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    plt.savefig(f'{output_dir}/saas_trifecta_index_{timestamp}.png', 
                dpi=300, bbox_inches='tight')
    plt.close()

async def analyze_and_plot_saas_trifecta_index():
    """
    Fetch data, create index, calculate returns, and generate visualizations
    """
    try:
        # Fetch company data
        company_data = await fetch_saas_trifecta_history()
        print(company_data)
        import pdb; pdb.set_trace() 
        # Create market cap weighted index
        index_df = create_saas_trifecta_index(company_data)
        
        # Calculate cumulative returns
        index_df = calculate_index_returns(index_df)
        
        # Export to CSV
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        csv_filename = f'exports/saas_trifecta_index_returns_{timestamp}.csv'
        index_df.to_csv(csv_filename, index=False)
        print(f"\nIndex data exported to {csv_filename}")
        
        # Create and save plots
        plot_index_performance(index_df)
        print("\nIndex performance plots have been saved to exports directory")
        
        return index_df
        
    except Exception as e:
        print(f"Error in SaaS Trifecta analysis: {str(e)}")
        raise


def plot_growth_metrics(df: pd.DataFrame, output_dir: str = 'exports') -> None:
    """
    Create and save bar plots for revenue and cash flow growth metrics
    
    Args:
        df: DataFrame containing the metrics
        output_dir: Directory to save the plots
    """
    # Set style
    plt.style.use('seaborn-v0_8')
    
    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Revenue Growth Plot
    sns.barplot(data=df, x='quarter', y='Revenue YoY Growth (%)', 
                hue='ticker', ax=ax1)  # Add hue parameter
    ax1.set_title('Revenue Year-over-Year Growth')
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45)
    ax1.axhline(y=0, color='r', linestyle='--', alpha=0.3)
    ax1.legend(title='SaaS Trifecta', bbox_to_anchor=(1.05, 1), loc='upper left')  # Add legend
    
    # Cash Flow Growth Plot
    sns.barplot(data=df, x='quarter', y='Cash Flow YoY Growth (%)', 
                hue='ticker', ax=ax2)  # Add hue parameter
    ax2.set_title('Operating Cash Flow Year-over-Year Growth')
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45)
    ax2.axhline(y=0, color='r', linestyle='--', alpha=0.3)
    ax2.legend(title='SaaS Trifecta', bbox_to_anchor=(1.05, 1), loc='upper left')  # Add legend
    
    # Adjust layout with more space for legends
    plt.tight_layout()
    
    # Save plots
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    plt.savefig(f'{output_dir}/growth_metrics_{timestamp}.png', dpi=300, bbox_inches='tight')
    plt.close()

# Modify the analyze_saas_companies function to include visualization
async def analyze_and_plot_saas_companies():
    """
    Analyze SaaS companies' metrics, save results to CSV, and generate visualization plots.
    
    Returns:
        tuple: (company_dfs, combined_df) containing individual and combined company metrics
    """
    try:
        # Reference to existing code that gets company_dfs and combined_df
        company_dfs, combined_df = await analyze_saas_companies()
        
        # Save combined metrics to CSV
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        csv_filename = f'exports/combined_saas_metrics_{timestamp}.csv'
        combined_df.to_csv(csv_filename, index=False)
        print(f"\nData exported to {csv_filename}")
        
        # Create and save plots
        plot_growth_metrics(combined_df)
        print("\nGrowth metrics plots have been saved to exports directory")
        
        return company_dfs, combined_df
        
    except Exception as e:
        print(f"Error in SaaS analysis: {str(e)}")
        raise
    
if __name__ == "__main__":
    asyncio.run(analyze_and_plot_saas_companies())
    asyncio.run(analyze_and_plot_saas_trifecta_index())