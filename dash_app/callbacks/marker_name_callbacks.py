from dash import Output, Input, Dash

def register_marker_name_callbacks(app: Dash):

    @app.callback(
    Output('selected-marker-trajectory', 'children'),
    [Input('store-selected-marker', 'data')]    
    )
    def update_selected_marker(stored_data):
        return stored_data['marker'] if stored_data else None

    @app.callback(
        Output('selected-marker-absolute-error', 'children'),
        [Input('store-selected-marker', 'data')]
    )
    def update_absolute_error_marker(stored_data):
        return stored_data['marker'] if stored_data else None

    @app.callback(
        Output('selected-marker-shading-error', 'children'),
        [Input('store-selected-marker', 'data')]
    )
    def update_shading_error_marker(stored_data):
        return stored_data['marker'] if stored_data else None

    @app.callback(
        Output('selected-marker-info-card', 'children'),
        [Input('store-selected-marker', 'data')]
    )
    def update_info_marker(stored_data):
        return stored_data['marker'] if stored_data else None

