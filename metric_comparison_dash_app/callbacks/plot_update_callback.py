from dash import Output, Input, Dash, State, ALL
from dash_app.plotting.joint_trajectory_plots import create_dash_trajectory_plots
from dash_app.plotting.joint_velocity_plots import create_dash_velocity_plots
from dash_app.plotting.absolute_error_plots import create_absolute_error_plots
from dash_app.plotting.shaded_error_plots import create_shaded_error_plots

from models.mocap_data_model import MoCapData

def register_plot_update_callback(app: Dash, position_data_and_error:MoCapData, velocity_data_and_error:MoCapData, COLOR_OF_CARDS):
    """
    Register callbacks related to updating plots in the Dash application.

    Args:
        app (Dash): The Dash application instance.
        position_data_and_error (MoCapData): Data model containing position data and error metrics.
        velocity_data_and_error (MoCapData): Data model containing velocity data and error metrics.
        COLOR_OF_CARDS (str): Hex color code for card backgrounds.
    """

    @app.callback(
        Output('trajectory-plots', 'children'),
        [Input('store-selected-marker', 'data')],
    )
    def update_trajectory_plot(stored_data):
        """
        Update the trajectory plots based on the selected marker.

        Args:
            stored_data (dict): Data stored in Dash dcc.Store component, containing the selected marker.

        Returns:
            list: A list of Dash components representing trajectory plots.
        """
        selected_marker = stored_data['marker'] if stored_data else None
        return create_dash_trajectory_plots(selected_marker, position_data_and_error.joint_dataframe, COLOR_OF_CARDS)
    
    @app.callback(
        Output('velocity-plots', 'children'),
        [Input('store-selected-marker', 'data')],
    )
    def update_velocity_plot(stored_data):
        """
        Update the velocity plots based on the selected marker.

        Args:
            stored_data (dict): Data stored in Dash dcc.Store component, containing the selected marker.

        Returns:
            list: A list of Dash components representing velocity plots.
        """
        selected_marker = stored_data['marker'] if stored_data else None
        return create_dash_velocity_plots(selected_marker, velocity_data_and_error.joint_dataframe, COLOR_OF_CARDS)
    
    @app.callback(
        Output('error-plots', 'children'),
        [Input('store-selected-marker', 'data')]
    )
    def update_absolute_error_plot(stored_data):
        """
        Update the absolute error plots based on the selected marker.

        Args:
            stored_data (dict): Data stored in Dash dcc.Store component, containing the selected marker.

        Returns:
            list: A list of Dash components representing absolute error plots.
        """
        selected_marker = stored_data['marker'] if stored_data else None
        return create_absolute_error_plots(selected_marker, position_data_and_error.absolute_error_dataframe, COLOR_OF_CARDS)
    
    @app.callback(
        Output('error-shading-plots', 'children'),
        [Input('store-selected-marker', 'data')]
    )
    def update_shaded_error_plot(stored_data):
        """
        Update the error shading plots based on the selected marker.

        Args:
            stored_data (dict): Data stored in Dash dcc.Store component, containing the selected marker.

        Returns:
            list: A list of Dash components representing error shading plots.
        """
        selected_marker = stored_data['marker'] if stored_data else None
        return create_shaded_error_plots(selected_marker, position_data_and_error.joint_dataframe, position_data_and_error.absolute_error_dataframe, COLOR_OF_CARDS)
