import dash_bootstrap_components as dbc
from dash import html, dcc

def get_info_card(color_of_cards):
    card_content = dbc.Card([
        dbc.CardHeader("Selected Marker:"),
        dbc.CardBody(
            [
                dbc.Row([dbc.Label(id='selected-marker-info-card', className = 'text-info', style={'font-weight': 'bold'})]),
                dbc.Row([
                    dbc.Label("X RMSE:", className="card-text", style={'color':'darkred','font-weight': 'bold'}),
                    dbc.Label(id='info-x-rmse', className="card-text"),
                ]),
                dbc.Row([
                    dbc.Label("Y RMSE:", className="card-text", style={'color':'darkgreen','font-weight': 'bold'}),
                    dbc.Label(id='info-y-rmse', className="card-text"),
                ]),
                dbc.Row([
                    dbc.Label("Z RMSE:", className="card-text", style={'color':'darkblue','font-weight': 'bold'}),
                    dbc.Label(id='info-z-rmse', className="card-text"),
                ])
            ]
        ),
    ], className="mb-4 mt-4")

    save_button = dbc.Button("Save Report", id="save-report-btn", color="primary", className="mb-2")
    download_component = dcc.Download(id="download-report")

    
    return html.Div([
        card_content,
        html.Div(save_button, style={'textAlign': 'center'}),  # Button below the card
        download_component
    ], style={
        'position': 'fixed',
        'top': '0',
        'right': '0',
        'height': '100vh',
        'overflow-y': 'auto',  
        'z-index': 1000,  
        'backgroundColor': color_of_cards
    })

