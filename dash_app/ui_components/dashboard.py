from .scatter_plot_UI import create_3d_figure_from_subsampled_data
from .indicators import create_indicators_ui
from .marker_buttons_list import create_marker_buttons

from dash_app.plotting.rmse_joint_plot import create_rmse_joint_bar_plot

import numpy as np

#this page handles updating of anything that appears on the dashboard 

def prepare_dashboard_elements(dataframe_of_3d_data, rmse_dataframe, frame_skip_interval, color_of_cards):
    """Prepare the figures and components for the Dash app layout."""
    scatter_3d_figure = create_3d_figure_from_subsampled_data(dataframe_of_3d_data, frame_skip_interval, color_of_cards)
    indicators = create_indicators_ui(rmse_dataframe)
    marker_buttons_list = create_marker_buttons(dataframe_of_3d_data)
    joint_rmse_plot = create_rmse_joint_bar_plot(rmse_dataframe)

    return scatter_3d_figure, indicators, marker_buttons_list, joint_rmse_plot


def update_joint_marker_card(selected_marker, rmse_dataframe):
    rmses_for_this_marker = rmse_dataframe[rmse_dataframe.marker == selected_marker][['coordinate','RMSE']]
    rmses_dataframe_with_coordinate_as_index = rmses_for_this_marker.set_index('coordinate')
    x_error_rmse = np.round(rmses_dataframe_with_coordinate_as_index.at['x_error', 'RMSE'],2)
    y_error_rmse = np.round(rmses_dataframe_with_coordinate_as_index.at['y_error', 'RMSE'],2)
    z_error_rmse = np.round(rmses_dataframe_with_coordinate_as_index.at['z_error', 'RMSE'],2)

    return x_error_rmse, y_error_rmse, z_error_rmse


def update_marker_buttons(marker, button_ids):

    # Use list comprehension to construct updated_classnames
    updated_classnames = [
        'btn btn-info' if button_id['index'] == marker else
        'btn btn-dark'
        for button_id in button_ids
    ]
    
    return updated_classnames
