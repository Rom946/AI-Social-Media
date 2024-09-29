from dash import Dash, dcc, html  # Updated imports
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd

# Define the layout of the Dash app
def init_dash_analytics(server, posts):
    # Convert posts data to DataFrame
    data = {
        'post_id': [post['id'] for post in posts],
        'likes': [post['likes'] for post in posts],
        'dislikes': [post['dislikes'] for post in posts],
        'comments': [len(post['comments']) for post in posts]
    }
    df = pd.DataFrame(data)

    dash_app = Dash(__name__, server=server, url_base_pathname='/analytics_dash/')
    dash_app.layout = html.Div([
        html.H1("Analytics Dashboard"),
        dcc.Graph(
            id='likes-bar',
            figure=px.bar(df, x='post_id', y='likes', title='Likes per Post')
        ),
        dcc.Graph(
            id='dislikes-bar',
            figure=px.bar(df, x='post_id', y='dislikes', title='Dislikes per Post')
        ),
        dcc.Graph(
            id='comments-bar',
            figure=px.bar(df, x='post_id', y='comments', title='Comments per Post')
        )
    ])
    return dash_app