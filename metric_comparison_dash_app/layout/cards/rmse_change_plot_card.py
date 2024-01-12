from .create_card import create_card
from dash import dcc

def get_rmse_change_plot_card(rmse_change_plot, color_of_cards):
    content = [dcc.Graph(id=f'rmse-change-figure', figure=rmse_change_plot)]
    return create_card("Change in RMSE", content, color_of_cards)