from dash_app.report_generation.report_syles import styles
from dash_app.report_generation.html_report_utils import fig_to_html, generate_rmse_table, create_subplots_from_individual_figs, create_indicators

from dash_app.data_utils.extract_rmse_values import extract_overall_rmse_values_from_dataframe
from dash_app.plotting.indicator_plot import create_indicator
from dash_app.ui_components.dashboard import update_joint_marker_card
from dash_app.plotting.rmse_joint_plot import create_rmse_joint_bar_plot, create_position_velocity_rmse_joint_bar_plot
from dash_app.plotting.joint_trajectory_plots import create_joint_trajectory_plots
from dash_app.plotting.joint_velocity_plots import create_joint_velocity_plots


def generate_navigation_links(unique_markers):
    navigation_html = "<div class='navigation'>"
    for marker in unique_markers:
        navigation_html += f"<a href='#{marker}'>{marker}</a> "
    navigation_html += "</div>"
    return navigation_html

def generate_overall_rmse_indicators_html(rmse_dataframe):
    rmse_indicators_html = "<div class='indicators-container'>"
    rmse_values = extract_overall_rmse_values_from_dataframe(rmse_dataframe)
    indicators = create_indicators(rmse_values)
    f = 2
    for indicator in indicators:
        indicator_html = fig_to_html(indicator)
        rmse_indicators_html += f"<div class='indicator-wrapper'>{indicator_html}</div>"
    rmse_indicators_html += "</div>"

    return rmse_indicators_html

def generate_overall_joint_rmse_bar_plot(position_rmse_dataframe, velocity_rmse_dataframe):
    rmse_barplot_html = ""
    # rmse_joint_bar_plot = create_rmse_joint_bar_plot(rmse_dataframe)
    rmse_joint_bar_plot = create_position_velocity_rmse_joint_bar_plot(position_rmse_dataframe, velocity_rmse_dataframe)
    for plot_label, rmse_plot in rmse_joint_bar_plot.items():
        rmse_plot.update_layout(height=300)
        rmse_barplot_html += fig_to_html(rmse_plot)
    return rmse_barplot_html
    

def generate_marker_specific_html(marker, position_dataframe_of_3d_data, position_rmse_dataframe, velocity_dataframe_of_3d_data, velocity_rmse_dataframe):

    marker_specific_html = f"<div class='marker-section' id='{marker}'><center><h1>{marker}</h1></center>"

    # Get RMSE values for this marker and generate table
    marker_position_rmse_values = {
        'x': update_joint_marker_card(marker, position_rmse_dataframe)[0],
        'y': update_joint_marker_card(marker, position_rmse_dataframe)[1],
        'z': update_joint_marker_card(marker, position_rmse_dataframe)[2]
    }

    marker_velocity_rmse_values = {
        'x': update_joint_marker_card(marker, velocity_rmse_dataframe)[0],
        'y': update_joint_marker_card(marker, velocity_rmse_dataframe)[1],
        'z': update_joint_marker_card(marker, velocity_rmse_dataframe)[2]
    }

    rmse_position_table_html = generate_rmse_table(marker_position_rmse_values)
    marker_specific_html += rmse_position_table_html  # Add the table to the content

    rmse_velocity_table_html = generate_rmse_table(marker_velocity_rmse_values)
    marker_specific_html += rmse_velocity_table_html  # Add the table to the content

    marker_specific_html += f"<center><h2> Position Comparison (mm) </h1></center>"
    fig_x, fig_y, fig_z = create_joint_trajectory_plots(marker, position_dataframe_of_3d_data, color_of_cards='white')
    figure = create_subplots_from_individual_figs(fig_x, fig_y, fig_z, color_of_cards='white')
    marker_specific_html += fig_to_html(figure)

    marker_specific_html += f"<center><h2> Velocity Comparison (mm/frame) </h1></center>"
    fig_x_vel, fig_y_vel, fig_z_vel = create_joint_velocity_plots(marker, velocity_dataframe_of_3d_data, color_of_cards='white')
    figure_vel = create_subplots_from_individual_figs(fig_x_vel, fig_y_vel, fig_z_vel, color_of_cards='white')
    # Convert figures to HTML and add to the report content
    marker_specific_html += fig_to_html(figure_vel)

    marker_specific_html += "</div>"  # Ends the section for a specific marker

    return marker_specific_html


def generate_html_report(position_dataframe_of_3d_data, position_rmse_dataframe, velocity_dataframe_of_3d_data, velocity_rmse_dataframe, filename="trajectory_report.html"):
    unique_markers = position_dataframe_of_3d_data['marker'].unique()

    # Start of the HTML content with included CSS for styling
    html_content = f"<html><head><title>Trajectory Report</title>{styles}</head><body>"
    
    html_content += generate_navigation_links(unique_markers)

    html_content += generate_overall_rmse_indicators_html(position_rmse_dataframe)

    html_content += generate_overall_joint_rmse_bar_plot(position_rmse_dataframe, velocity_rmse_dataframe)

    for marker in unique_markers:
        html_content += generate_marker_specific_html(marker, position_dataframe_of_3d_data, position_rmse_dataframe, velocity_dataframe_of_3d_data, velocity_rmse_dataframe)

    html_content += "</body></html>"

    return html_content

    # with open(filename, "w", encoding='utf-8') as file:
    #     file.write(html_content)
    # print(f"Report saved as {filename}")
