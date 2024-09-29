from dash import Dash, dcc, html  # Import necessary Dash components
import plotly.express as px  # Import Plotly for data visualization
from dash.dependencies import Input, Output  # Import Dash dependencies for callbacks
import pandas as pd  # Import pandas for data manipulation
import numpy as np  # Import numpy for numerical operations
import schedule  # Import schedule for scheduling tasks
import time  # Import time for sleep
import threading  # Import threading for running the scheduler
from app.utils.trending_topics import TrendingTopicsFetcher  # Import the TrendingTopicsFetcher class
import logging  # Import logging for error handling

# Create an instance of TrendingTopicsFetcher
trending_topics_fetcher = TrendingTopicsFetcher()

# Function to get trending searches and metrics
def get_trending_metrics():
    metrics = []
    all_trends = trending_topics_fetcher.get_trending_topics()

    # Process Google trends
    if 'google' in all_trends:
        for search in all_trends['google']:
            try:
                # Build the payload for the search term
                trending_topics_fetcher.pytrends.build_payload([search], cat=0, timeframe='now 1-d', geo='', gprop='')
                # Get the interest over time data
                interest_over_time_df = trending_topics_fetcher.pytrends.interest_over_time()
                if not interest_over_time_df.empty:
                    # Handle FutureWarning by using infer_objects
                    interest_over_time_df = interest_over_time_df.infer_objects()
                    # Calculate search volume and growth rate
                    search_volume = interest_over_time_df[search].sum()
                    initial_value = interest_over_time_df[search].iloc[0]
                    final_value = interest_over_time_df[search].iloc[-1]
                    growth_rate = ((final_value - initial_value) / initial_value * 100) if initial_value != 0 else np.nan  # Handle division by zero
                    metrics.append({
                        'term': search,
                        'search_volume': search_volume,
                        'growth_rate': growth_rate
                    })
            except Exception as e:
                logging.error(f"Error processing Google trend {search}: {str(e)}", exc_info=True)

    # Process Bing trends
    if 'bing' in all_trends:
        for search in all_trends['bing']:
            metrics.append({
                'term': search,
                'search_volume': np.nan,  # Placeholder as we don't have search volume data from Bing
                'growth_rate': np.nan  # Placeholder as we don't have growth rate data from Bing
            })

    return metrics

# Function to update trending searches and metrics
def update_trending_searches():
    global df
    metrics = get_trending_metrics()
    df = pd.DataFrame(metrics)
    print("Updated trending searches and metrics")  # Debug print

# Schedule the update_trending_searches function to run every day at a specific time
schedule.every().day.at("00:00").do(update_trending_searches)

# Keep the script running
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Get initial metrics
metrics = get_trending_metrics()

# Create a DataFrame for Plotly
df = pd.DataFrame(metrics)

# Define the layout of the Dash app
def init_dash_top_trends(server):
    dash_app = Dash(__name__, server=server, url_base_pathname='/dash/')
    dash_app.layout = html.Div([
        html.H1("Top 10 Trending Searches"),
        html.P(f"Bing API Calls This Month: {trending_topics_fetcher.bing_api_call_count}"),
        dcc.Graph(
            id='trending-searches-bar',
            figure=px.bar(df, x='term', y='search_volume', title='Search Volume of Top 10 Trending Searches')
        ),
        dcc.Graph(
            id='trending-searches-line',
            figure=px.line(df, x='term', y='growth_rate', title='Growth Rate of Top 10 Trending Searches')
        )
    ])
    return dash_app

# Start the scheduler in a separate thread
scheduler_thread = threading.Thread(target=run_scheduler)
scheduler_thread.start()