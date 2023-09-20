from dash import Output, Input, Dash
from dash_app.ui_components.dashboard import update_joint_marker_card

def register_info_card_callback(app: Dash, rmse_dataframe):
    @app.callback(
        [Output('info-x-rmse', 'children'),
        Output('info-y-rmse', 'children'),
        Output('info-z-rmse', 'children')],
        [Input('store-selected-marker', 'data')]
    )
    def update_info_card(stored_data):
        marker = stored_data['marker'] if stored_data else None
        x_rmse, y_rmse, z_rmse = update_joint_marker_card(marker, rmse_dataframe)
        return x_rmse, y_rmse, z_rmse