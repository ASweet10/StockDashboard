from dash import html
import dash_bootstrap_components as dbc

from Metric_Links import *

# Basic info card
def return_basic_info_card():
    card = dbc.Card([
            dbc.CardBody([
                html.Div([
                    dbc.Row(
                        dbc.Col(html.H5("", id="stock-name", style={'text-align':'center', 'font-weight': 'bold'}))
                    ),
                    dbc.Row(
                        dbc.Col(html.H6(id='stock-price'))
                    ),
                    dbc.Row(
                        dbc.Col(html.H6(id="stock-analyst-price"))
                    ),
                    dbc.Row(
                        dbc.Col(html.H6(id="stock-sector"))
                    ),
                    dbc.Row(
                        dbc.Col(html.H6(id="stock-industry"))
                    )
                ])
            ])
        ], style={'background-color': 'transparent', 'border': 'none', })
    return card

# Main metric functions
def return_marketcap_with_hover():
    div = html.Div([
        dbc.Row([
            dbc.Col([
                html.P([
                        html.A(
                            "Market Cap: ",
                            id="market-cap-anchor",
                            href=marketcap_Link,
                            target="_blank",
                            style={"textDecoration": "underline", "cursor": "pointer", "text-align": "left"},
                        )
                ]),
            dbc.Tooltip("Total value of company's stock. Number of shares * price", target="market-cap-anchor")
            ], className="col-md-5",),
            dbc.Col([
                html.P("", id="market-cap", style={'color': 'white', 'fontSize': '16', 'text-align':'left'})
            ], className="col-md-1")
        ])
    ])
    return div

def return_eps_with_hover():
    div = html.Div([
        dbc.Row([
            dbc.Col([
                html.P([
                        html.A(
                            "EPS: ",
                            id="eps-anchor",
                            href=eps_Link,
                            target="_blank",
                            style={"textDecoration": "underline", "cursor": "pointer", "text-align": "left"},
                        )
                ]),
            dbc.Tooltip("Indicator of profitability. Company profit / number of shares", target="eps-anchor")
            ], className="col-md-5",),
            dbc.Col([
                html.P("", id="eps", style={'color': 'white', 'fontSize': '16', 'text-align':'left'})
            ], className="col-md-1")
        ])
    ])
    return div

def return_ebitda_with_hover():
    div = html.Div([
        dbc.Row([
            dbc.Col([
                html.P([
                        html.A(
                            "EBITDA: ",
                            id="ebitda-ratio-anchor",
                            href=peRatio_Link,
                            target="_blank",
                            style={"textDecoration": "underline", "cursor": "pointer", "text-align": "left"},
                        )
                ]),
            dbc.Tooltip("Earnings before (I)nterest, (T)axes, (D)epreciation, and (A)mortization", target="ebitda-ratio-anchor")
            ], className="col-md-5",),
            dbc.Col([
                html.P("", id="ebitda", style={'color': 'white', 'fontSize': '16', 'text-align':'left'})
            ], className="col-md-1")
        ])
    ])
    return div

def return_peRatio_with_hover():
    div = html.Div([
        dbc.Row([
            dbc.Col([
                html.P([
                        html.A(
                            "P/E Ratio: ",
                            id="pe-ratio-anchor",
                            href=peRatio_Link,
                            target="_blank",
                            style={"textDecoration": "underline", "cursor": "pointer", "text-align": "left"},
                        )
                ]),
            dbc.Tooltip("Relative value of shares. Price / Earnings per share", target="pe-ratio-anchor")
            ], className="col-md-5",),
            dbc.Col([
                html.P("", id="pe-ratio", style={'color': 'white', 'fontSize': '16', 'text-align':'left'})
            ], className="col-md-1")
        ])
    ])
    return div

def return_peGRatio_with_hover():
    div = html.Div([
        dbc.Row([
            dbc.Col([
                html.P([
                        html.A(
                            "PEG Ratio: ",
                            id="peg-ratio-anchor",
                            href=peGRatio_Link,
                            target="_blank",
                            style={"textDecoration": "underline", "cursor": "pointer", "text-align": "left"},
                        )
                ]),
            dbc.Tooltip("Determine value while considering growth. P/E ratio / Growth in earnings", target="peg-ratio-anchor")
            ], className="col-md-5",),
            dbc.Col([
                html.P("", id="peg-ratio", style={'color': 'white', 'fontSize': '16', 'text-align':'left'})
            ], className="col-md-1")
        ])
    ])
    return div

def return_divYield_with_hover():
    div = html.Div([
        dbc.Row([
            dbc.Col([
                html.P([
                        html.A(
                            "Dividend Yield: ",
                            id="div-yield-ratio-anchor",
                            href=divYield_Link,
                            target="_blank",
                            style={"textDecoration": "underline", "cursor": "pointer", "text-align": "left"},
                        )
                ]),
            dbc.Tooltip("Dividends paid per share (annually) / share price. Displayed as %.", target="div-yield-ratio-anchor")
            ], className="col-md-5",),
            dbc.Col([
                html.P("", id="div-yield", style={'color': 'white', 'fontSize': '16', 'text-align':'left'})
            ], className="col-md-1")
        ])
    ])
    return div

def return_price_to_book_with_hover():
    div = html.Div([
        dbc.Row([
            dbc.Col([
                html.P([
                        html.A(
                            "Price-to-Book Ratio: ",
                            id="price-book-ratio-anchor",
                            href=priceToBook_Link,
                            target="_blank",
                            style={"textDecoration": "underline", "cursor": "pointer", "text-align": "left"},
                        )
                ]),
            dbc.Tooltip("Compares market cap to book value (net assets) of company", target="price-book-ratio-anchor")
            ], className="col-md-5",),
            dbc.Col([
                html.P("", id="price-book", style={'color': 'white', 'fontSize': '16', 'text-align':'left'})
            ], className="col-md-1")
        ])
    ])
    return div
    
def return_beta_with_hover():
    div = html.Div([
        dbc.Row([
            dbc.Col([
                html.P([
                        html.A(
                            "Beta: ",
                            id="beta-anchor",
                            href=beta_Link,
                            target="_blank",
                            style={"textDecoration": "underline", "cursor": "pointer", "text-align": "left"},
                        )
                ]),
            dbc.Tooltip("Compares volatility to index (1). Greater than 1, more volatile, and vice versa", target="beta-anchor")
            ], className="col-md-5",),
            dbc.Col([
                html.P("", id="beta", style={'color': 'white', 'fontSize': '16', 'text-align':'left'})
            ], className="col-md-1")
        ])
    ])
    return div

# News cards  
def return_news_card(news_title, news_description, news_url, image_source_url):
    card = dbc.Card(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.A(news_title, href=news_url, target="_blank",
                        style={'font-size':'18', 'font-weight': 'bold', 'text-align':'center'}),
                        dbc.CardImg(src=image_source_url,style={'text-align':'center'})
                    ],
                    className="col-md-5"
                ),
                dbc.Col(
                    dbc.CardBody(
                        [
                            html.P(news_description, style={'font-size':'12'})
                        ]
                    ),
                    className="col-md-7"
                ),
            ],
            className="g-0 d-flex align-items-center"
        )
    ],
    className="mb-3 p-4"
    )

    return card