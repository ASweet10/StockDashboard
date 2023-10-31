# Locally: Run app with `python sip_dashboard.py`
# http://127.0.0.1:8050/

# https://www.youtube.com/watch?v=XWJBJoV5yww    Render.com deployment guide

import os
import pandas as pd
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as pgo
import requests
import plotly.express as px
from datetime import datetime
from dateutil.relativedelta import relativedelta
import dash_loading_spinners as dls

import finnhub
from newsapi import *

from Dashboard_Layout import *
from BasicInfo_Layout import *
from dotenv import load_dotenv
load_dotenv()

#Initialize Dash App
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
app.config.suppress_callback_exceptions = True
server = app.server # For DashTools render

ALPHA_KEY = str(os.getenv('ALPHA_VANTAGE_KEY'))
NEWS_KEY = str(os.getenv('NEWS_API_KEY'))
FINNHUB_KEY = str(os.getenv('FINNHUB_API_KEY'))
api_url = "https://www.alphavantage.co/query?function="

# Changed from html.div to dbc.Container: https://stackoverflow.com/questions/75137777/there-is-a-horizontal-scrollbar-dasboard-plotly
#  Fixed horizontal scrollbar error & improved spacing
app.layout = dbc.Container(
    [
       dbc.Row(dbc.Col(html.H2('StockAnalysis', id='stock-ticker', style={'text-align':'center'}))),
       dbc.Row(dbc.Col(html.Div(return_input_bar(), style={'margin':'auto'}))),
       dbc.Row(),
       dbc.Row(
           [
               dbc.Col(
                   html.Div(
                       [
                            return_basic_info_card(),    # Basic info card (name, price, etc.)
                            dbc.Row([    # Metrics with links
                                dbc.Col([
                                    return_marketcap_with_hover(),
                                    return_peRatio_with_hover(),
                                    return_peGRatio_with_hover(),
                                    return_price_to_book_with_hover(),
                                ]),
                                dbc.Col([
                                    return_eps_with_hover(),
                                    return_divYield_with_hover(),
                                    return_beta_with_hover(),
                                    return_ebitda_with_hover(),
                                ])
                            ])
                       ]), width=6, style={"padding": "10px 10px 10px 10px"}),
                dbc.Col(
                   [
                       dls.Hash(
                        dcc.Graph(id='stock-price-graph', config={'displayModeBar': False}),
                        color="#435278",
                        speed_multiplier=2,
                        size=100,
                        fullscreen=True,
                       ),
                        return_timeinterval(),   # Time radio buttons

                   ], width=6, style={"padding": "10px 10px 10px 10px"}) # End col
            ]
       ),
       dbc.Row(
           [

                dbc.Col(
                    [
                        #dcc.Graph(id='bar-graph', config={'displayModeBar': False}),
                        dcc.Graph(id='pie-chart')
                    ], width=6),
                dbc.Col(
                    [
                        dcc.Graph(id='volume-graph', config={'displayModeBar': False})
                    ], width=6)
            ], style={"padding": "0px 20px 20px 20px"}
        ),
        dbc.Row(
            [
                dbc.Col(   # News module
                    html.Div([
                        html.Div(id='news-card-one'),
                        html.Div(id='news-card-two'),
                        html.Div(id='news-card-three')
                    ], 
                    ), width=10, style={'justify-content': 'center', 'background-color': 'transparent'}), # Remove background between cards
            ], style={'background-color': 'transparent', 'justify-content': 'center'}
        )
    ],
)           

#Input: State of time radio bar and searchbar (value entered)
# Called: When input button is pressed
#  Returns: Table, graph, and general info
@app.callback(Output('stock-name', 'children'), # Stock Name & (Ticker)
                Output('stock-ticker', 'children'), # Stock ticker above searchbar
                Output('stock-analyst-price', 'children'), # Analyst stock price
                Output('market-cap', 'children'), # Market Cap
                Output('eps', 'children'), # EPS
                Output('price-book', 'children'), # Price-to-Book Ratio
                Output('ebitda', 'children'), # EBITDA
                Output('pe-ratio', 'children'), # P/E Ratio
                Output('peg-ratio', 'children'), # (P/E)/Growth Ratio
                Output('div-yield', 'children'), # Dividend yield %
                Output('beta', 'children'), # Beta
                Output('stock-sector', 'children'), # Sector
                Output('stock-industry', 'children'), #Industry
                Output('stock-price-graph', 'figure'), # Price graph
                Output('pie-chart', 'figure'), # Sentiment graph
                Output('volume-graph', 'figure'), # Volume graph
                Output('news-card-one', 'children'),
                Output('news-card-two', 'children'), 
                Output('news-card-three', 'children'),
                [Input('ticker-input-button', 'n_clicks')], # Input button fires callback
                [State('time-interval-radio', 'value')], # Take radio value state
                [State('ticker-input-searchbar', 'value')], # Take input searchbar state
                prevent_initial_call = True)

# Called whenever ANY included inputs are changed
#  State: Allows you to pass extra values without firing the callback function
def return_dashboard(n_clicks, time_value, ticker):
    
    overview_response = requests.get(api_url + "OVERVIEW&symbol=" + ticker + "&apikey=" + ALPHA_KEY)
    overview_json = overview_response.json()

    stock_name = str(overview_json.get('Name'))
    stock_market_cap = overview_json.get('MarketCapitalization')
    stock_market_cap = int(stock_market_cap)
    stock_market_cap = '${:,}'.format(stock_market_cap)
    stock_eps = overview_json.get('EPS')
    stock_pe_ratio = overview_json.get('PERatio')
    stock_peg_ratio = overview_json.get('PEGRatio')
    stock_div_yield = float(overview_json.get('DividendYield'))
    stock_div_yield = '{:.1%}'.format(stock_div_yield)
    stock_ebitda = overview_json.get('EBITDA')
    stock_ebitda = int(stock_ebitda)
    stock_ebitda = '${:,}'.format(stock_ebitda)
    stock_priceBookRatio = overview_json.get('PriceToBookRatio')
    stock_beta = overview_json.get('Beta')

    # News section
    news_client = NewsApiClient(api_key=NEWS_KEY)
    news_dict = news_client.get_everything(qintitle=ticker, q=stock_name, language="en")

    #articleTitles = []
    #articleDescriptions = []
    #articleURLs = []
    #articleImages = []
#
    #for i in range(2):
    #    articleTitles[i] = news_dict['articles'][i]['title']
    #    articleDescriptions[i] = news_dict['articles'][i]['description']
    #    articleURLs[i] = news_dict['articles'][i]['url']
    #    articleImages[i] = news_dict['articles'][i]['urlToImage']
    #    print (articleTitles[i])
    #    print (articleDescriptions[i])
    #    print (articleImages[i])
    #    print (articleURLs[i])
    #
    #news_card_one = return_news_card(articleTitles[0], articleDescriptions[0], articleURLs[0], articleImages[0])
    #news_card_two = return_news_card(articleTitles[1], articleDescriptions[1], articleURLs[1], articleImages[1])
    #news_card_three = return_news_card(articleTitles[2], articleDescriptions[2], articleURLs[2], articleImages[2])

    
    artOne_title = news_dict['articles'][0]['title']
    artOne_desc = news_dict['articles'][0]['description']
    artOne_url = news_dict['articles'][0]['url']
    artOne_urlImage = news_dict['articles'][0]['urlToImage']
#
    artTwo_title = news_dict['articles'][1]['title']
    artTwo_desc = news_dict['articles'][1]['description']
    artTwo_url = news_dict['articles'][1]['url']
    artTwo_urlImage = news_dict['articles'][1]['urlToImage']
#
    artThree_title = news_dict['articles'][2]['title']
    artThree_desc = news_dict['articles'][2]['description']
    artThree_url = news_dict['articles'][2]['url']
    artThree_urlImage = news_dict['articles'][2]['urlToImage']
#
    news_card_one = return_news_card(artOne_title, artOne_desc, artOne_url, artOne_urlImage)
    news_card_two = return_news_card(artTwo_title, artTwo_desc, artTwo_url, artTwo_urlImage)
    news_card_three = return_news_card(artThree_title, artThree_desc, artThree_url, artThree_urlImage)


    # Main price chart
    # Code common to all time periods:
    finnhub_client = finnhub.Client(api_key=FINNHUB_KEY)
    now = datetime.now()  # datetime object, current date/time
    now_unix = int(now.timestamp())

    # Time periods
    if time_value == '5D':
        five_days_ago_unix = now - relativedelta(days=5)
        five_days_ago_unix = int(five_days_ago_unix.timestamp())
        data = finnhub_client.stock_candles(ticker, 'D', five_days_ago_unix, now_unix)

        df = pd.DataFrame.from_dict(data)        
        df['t'] = pd.to_datetime(df['t'], unit='s') # Convert time column from UNIX to datetime

        stock_fig = px.line(df, x='t', y='c', template="plotly_dark", labels={'t': 'Date', 'c': 'Close'})
        volume_fig = return_volume_graph(df)
        stock_price = df['c'].iloc[-1]   
    
    elif time_value == '1mo':
        month_ago_unix = now - relativedelta(months=1)
        month_ago_unix = int(month_ago_unix.timestamp())
        data = finnhub_client.stock_candles(ticker, 'D', month_ago_unix, now_unix)

        df = pd.DataFrame.from_dict(data)
        df['t'] = pd.to_datetime(df['t'], unit='s') # Convert time column from UNIX to datetime

        stock_fig = px.line(df, x='t', y='c', template="plotly_dark", labels={'t': 'Date', 'c': 'Close'})
        volume_fig = return_volume_graph(df)
        stock_price = df['c'].iloc[-1] 

    elif time_value == '6mo':
        six_month_ago_unix = now - relativedelta(months=6)
        six_month_ago_unix = int(six_month_ago_unix.timestamp())
        data = finnhub_client.stock_candles(ticker, 'D', six_month_ago_unix, now_unix)

        df = pd.DataFrame.from_dict(data)
        df['t'] = pd.to_datetime(df['t'], unit='s') #Convert time column from UNIX to datetime

        stock_fig = px.line(df, x='t', y='c', template="plotly_dark", labels={'t': 'Date', 'c': 'Close'})
        volume_fig = return_volume_graph(df)
        stock_price = df['c'].iloc[-1]

    elif time_value == '3mo':
        three_month_ago_unix = now - relativedelta(months=3)
        three_month_ago_unix = int(three_month_ago_unix.timestamp())
        data = finnhub_client.stock_candles(ticker, 'D', three_month_ago_unix, now_unix)

        df = pd.DataFrame.from_dict(data)
        df['t'] = pd.to_datetime(df['t'], unit='s') #Convert time column from UNIX to datetime

        stock_fig = px.line(df, x='t', y='c', template="plotly_dark", labels={'t': 'Date', 'c': 'Close'})
        volume_fig = return_volume_graph(df)
        stock_price = df['c'].iloc[-1]

    elif time_value == 'ytd':
        nowDate = now.date()
        current_year = nowDate.year
        first_day_of_year = datetime(current_year, 1, 1).date()
        days_since_new_year = nowDate - first_day_of_year

        ytd_unix = now - relativedelta(days=days_since_new_year.days)
        ytd_unix = int(ytd_unix.timestamp())

        data = finnhub_client.stock_candles(ticker, 'D', ytd_unix, now_unix)

        df = pd.DataFrame.from_dict(data)
        df['t'] = pd.to_datetime(df['t'], unit='s') #Convert time column from UNIX to datetime

        stock_fig = px.line(df, x='t', y='c', template="plotly_dark", labels={'t': 'Date', 'c': 'Close'})
        volume_fig = return_volume_graph(df)
        stock_price = df['c'].iloc[-1]
    
    elif time_value == '1y':
        year_ago_unix = now - relativedelta(years=1)
        year_ago_unix = int(year_ago_unix.timestamp())
        data = finnhub_client.stock_candles(ticker, 'D', year_ago_unix, now_unix)

        df = pd.DataFrame.from_dict(data)
        df['t'] = pd.to_datetime(df['t'], unit='s') #Convert time column from UNIX to datetime

        stock_fig = px.line(df, x='t', y='c', template="plotly_dark", labels={'t': 'Date', 'c': 'Close'})
        volume_fig = return_volume_graph(df)
        stock_price = df['c'].iloc[-1]

        trends = finnhub_client.recommendation_trends(ticker)
        trend_df = pd.DataFrame.from_dict(trends)
        #trend_df = trend_df[trend_df.index == 0]
        bar_fig = return_sentiment_bar_graph(trend_df)      

    else:
        stock_fig = pgo.Figure(data=[])
        bar_fig = pgo.Figure(data=[])
        volume_fig = pgo.Figure(data=[])
        stock_price = '$Price_failed'
    
    stock_fig.update_yaxes(tickprefix = '$', tickformat = ',.2f', nticks=7)
    stock_fig.update_xaxes(title = '')
    stock_fig.update_layout(margin=dict(l=30, r=30, t=30, b=30)) # Remove white padding

    trends = finnhub_client.recommendation_trends(ticker)

    trend_df = pd.DataFrame.from_dict(trends)
    #bar_fig = return_sentiment_bar_graph(trend_df)
    pie_fig = return_sentiment_pie_chart(trend_df)
    
    #Basic stock info (top left of layout)
    name_and_price = stock_name + "        $" + str(stock_price)
    stock_ticker = ticker.upper()
    stock_sector = 'Sector: ' + str(overview_json.get('Sector'))
    stock_industry = 'Industry: ' + str(overview_json.get('Industry'))
    stock_target_price = 'Analyst target: $' + str(overview_json.get('AnalystTargetPrice'))



    #Return these values to output, in order
    return name_and_price, stock_ticker, stock_target_price, \
    stock_market_cap, stock_eps, \
    stock_priceBookRatio, stock_ebitda,  \
    stock_pe_ratio, stock_peg_ratio, stock_div_yield, stock_beta, \
    stock_sector, stock_industry, \
    stock_fig, pie_fig, volume_fig, \
    news_card_one, news_card_two, news_card_three

          
if __name__ == '__main__':
    app.run_server(debug=True)