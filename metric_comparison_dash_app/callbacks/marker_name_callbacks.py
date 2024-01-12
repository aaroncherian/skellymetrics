from dash import Output, Input, Dash

def register_marker_name_callbacks(app: Dash):
    """
    Register callbacks related to updating marker name display in various components of the Dash app.

    Args:
        app (Dash): The Dash application instance.
    """

    @app.callback(
        Output('selected-marker-trajectory', 'children'),
        [Input('store-selected-marker', 'data')]    
    )
    def update_selected_marker(stored_data):
        """
        Update the displayed selected marker name in the trajectory section.

        Args:
            stored_data (dict): Data stored in Dash dcc.Store component, containing the selected marker.

        Returns:
            str: The name of the selected marker.
        """
        return stored_data['marker'] if stored_data else None
    
