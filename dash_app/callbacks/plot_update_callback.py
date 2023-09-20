from dash import Output, Input, Dash, State, ALL
from dash_app.plotting.joint_trajectory_plots import create_joint_trajectory_plots
from dash_app.plotting.absolute_error_plots import create_absolute_error_plots
from dash_app.plotting.shaded_error_plots import create_shaded_error_plots


def register_plot_update_callback(app: Dash, dataframe_of_3d_data, absolute_error_dataframe, COLOR_OF_CARDS):

    @app.callback(
    Output('trajectory-plots', 'children'),
    [Input('store-selected-marker', 'data')]    ,
    )
    def update_trajectory_plot(stored_data):
        selected_marker = stored_data['marker'] if stored_data else None
        return create_joint_trajectory_plots(selected_marker, dataframe_of_3d_data, COLOR_OF_CARDS)
    
    @app.callback(
        Output('error-plots', 'children'),
        [Input('store-selected-marker', 'data')]
    )
    def update_absolute_error_plot(stored_data):
        selected_marker = stored_data['marker'] if stored_data else None
        return create_absolute_error_plots(selected_marker, absolute_error_dataframe, COLOR_OF_CARDS)
    
    @app.callback(
        Output('error-shading-plots', 'children'),
        [Input('store-selected-marker', 'data')]
    )
    def update_shaded_error_plot(stored_data):
        selected_marker = stored_data['marker'] if stored_data else None
        return create_shaded_error_plots(selected_marker, dataframe_of_3d_data, absolute_error_dataframe, COLOR_OF_CARDS)



        
