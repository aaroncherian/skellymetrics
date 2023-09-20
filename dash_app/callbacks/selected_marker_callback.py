import dash
from dash import Output, Input, State, Dash, ALL
import json

def register_selected_marker_callback(app: Dash):
    @app.callback(
    Output('store-selected-marker', 'data'),
    [Input('main-graph', 'clickData'),
        Input({'type': 'marker-button', 'index': ALL}, 'n_clicks')],
    [State('store-selected-marker', 'data')]
    )
    
    def update_stored_marker(clickData, marker_clicks, stored_data):
        ctx = dash.callback_context
        if not ctx.triggered:
            return dash.no_update
        
        input_id = ctx.triggered[0]['prop_id'].split('.')[0]
        selected_marker = stored_data.get('marker', None) if stored_data else None
        marker = get_selected_marker(input_id, clickData, selected_marker)
        return {'marker': marker}
    

def get_selected_marker(input_id, clickData, selected_marker):
    # If a marker button was clicked, use its index as the selected marker
    if 'marker-button' in input_id:
        marker = json.loads(input_id)['index']
    # If a marker was clicked in the main graph, use its ID as the selected marker
    elif clickData is not None and 'points' in clickData and len(clickData['points']) > 0 and 'id' in clickData['points'][0]:
        #check if click data exists, and that click data contains the 'points' key, and the 'id' key
        marker = clickData['points'][0]['id']
    # Otherwise, use the currently selected marker
    else:
        marker = selected_marker
    
    return marker