from .scatter_plot_UI import create_3d_figure_from_subsampled_data
from .indicators import create_indicators_ui
from .marker_buttons_list import create_marker_buttons

from metric_comparison_dash_app.plotting.rmse_change_plot import create_rmse_change_plot
import numpy as np
from models.mocap_data_model import MoCapData


#this page handles updating of anything that appears on the dashboard 

def prepare_dashboard_elements(position_dataframe, rmse_change_dataframe, frame_skip_interval, color_of_cards):
    """Prepare the figures and components for the Dash app layout."""
    scatter_3d_figure = create_3d_figure_from_subsampled_data(dataframe_of_3d_data=position_dataframe, frame_skip_interval=frame_skip_interval, color_of_cards=color_of_cards)
    # indicators = create_indicators_ui(position_data_and_error.rmse_dataframe)
    marker_buttons_list = create_marker_buttons(position_dataframe)
    rmse_change_plot = create_rmse_change_plot(rmse_change_dataframe)
    

    return scatter_3d_figure, rmse_change_plot, marker_buttons_list

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
