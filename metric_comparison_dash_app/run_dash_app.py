
from dash import Dash

import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

from metric_comparison_dash_app.data_utils.load_data import combine_freemocap_and_qualisys_into_dataframe
from metric_comparison_dash_app.data_utils.file_manager import FileManager

from metric_comparison_dash_app.ui_components.dashboard import prepare_dashboard_elements

from metric_comparison_dash_app.layout.main_layout import get_layout

from metric_comparison_dash_app.callbacks.marker_name_callbacks import register_marker_name_callbacks
from metric_comparison_dash_app.callbacks.selected_marker_callback import register_selected_marker_callback
from metric_comparison_dash_app.callbacks.info_card_callback import register_info_card_callback
from metric_comparison_dash_app.callbacks.plot_update_callback import register_plot_update_callback
from metric_comparison_dash_app.callbacks.marker_button_color_callback import register_marker_button_color_callback
from metric_comparison_dash_app.callbacks.report_download_callback import register_report_download_callback

from models.mocap_data_model import MoCapData

COLOR_OF_CARDS = '#F3F5F7'
FRAME_SKIP_INTERVAL = 5



def run_dash_app(position_dataframe):
    # Initialize Dash App
    app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])
    register_selected_marker_callback(app) #register a callback to find the selected marker and stored it
    register_marker_name_callbacks(app) #register a callback to update the marker name wherever it is listed in the app
    # register_info_card_callback(app, position_data_and_error.rmse_dataframe, velocity_data_and_error.rmse_dataframe)
    register_plot_update_callback(app, position_dataframe, COLOR_OF_CARDS)
    register_marker_button_color_callback(app)
    # register_report_download_callback(app, position_data_and_error.joint_dataframe, position_data_and_error.rmse_dataframe, velocity_data_and_error.joint_dataframe ,velocity_data_and_error.rmse_dataframe)

    load_figure_template('LUX')

    # Create Figures and Components
    scatter_3d_figure, marker_buttons_list = prepare_dashboard_elements(
        position_dataframe, FRAME_SKIP_INTERVAL, COLOR_OF_CARDS)

    # app.layout = get_layout(marker_figure=scatter_3d_figure,
    #                         joint_rmse_figure=joint_rmse_plot,
    #                         list_of_marker_buttons=marker_buttons_list,
    #                         indicators=indicators,
    #                         color_of_cards=COLOR_OF_CARDS)
    
    
    app.layout = get_layout(marker_figure=scatter_3d_figure,
                            list_of_marker_buttons=marker_buttons_list,
                            color_of_cards=COLOR_OF_CARDS)

    app.run_server(debug=False)


if __name__ == '__main__':

        
    from pathlib import Path

    path_to_recording_folder = Path(r"D:\2023-05-17_MDN_NIH_data\1.0_recordings\calib_3\sesh_2023-05-17_14_53_48_MDN_NIH_Trial3")

    file_manager = FileManager(path_to_recording_folder)
    freemocap_data = file_manager.freemocap_data
    qualisys_data = file_manager.qualisys_data
    rmse_dataframe = file_manager.rmse_dataframe
    absolute_error_dataframe = file_manager.absolute_error_dataframe
    dataframe_of_3d_data = combine_freemocap_and_qualisys_into_dataframe(freemocap_3d_data=freemocap_data, qualisys_3d_data=qualisys_data)

    run_dash_app(dataframe_of_3d_data, rmse_dataframe, absolute_error_dataframe)
        