import plotly.io as pio
from dash_app.plotting.joint_trajectory_plots import create_joint_trajectory_plots
from plotly.subplots import make_subplots

from dash_app.data_utils.extract_rmse_values import extract_overall_rmse_values_from_dataframe
from dash_app.plotting.indicator_plot import create_indicator
from dash_app.ui_components.dashboard import update_joint_marker_card


def create_subplots_from_individual_figs(fig_x, fig_y, fig_z, color_of_cards):
    # Create a subplot with 1 column and 3 rows
    fig = make_subplots(rows=3, cols=1, vertical_spacing=0.1)

    # Add traces for X, Y, and Z
    for i, single_fig in enumerate([fig_x, fig_y, fig_z], start=1):
        for trace in single_fig['data']:
            fig.add_trace(trace, row=i, col=1)

    # Update figure layout
    fig.update_layout(height=700, showlegend=True, paper_bgcolor=color_of_cards)
    fig.update_xaxes(title_text="Frame", row=3, col=1)  # Only the last plot (Z) shows the Frame on x-axis
    fig.update_yaxes(title_text="X Axis", row=1, col=1)
    fig.update_yaxes(title_text="Y Axis", row=2, col=1)
    fig.update_yaxes(title_text="Z Axis", row=3, col=1)

    return fig

def create_indicators(rmse_values):
    return [
        create_indicator(rmse_values['total'], "Total RMSE"),
        create_indicator(rmse_values['x'], "X RMSE", color_of_text='red'),
        create_indicator(rmse_values['y'], "Y RMSE", color_of_text='green'),
        create_indicator(rmse_values['z'], "Z RMSE", color_of_text='blue'),
    ]

def fig_to_html(fig):
    return pio.to_html(fig, full_html=False)

def generate_rmse_table(rmse_values):
    table_html = '<table>'
    # Add a title row
    table_html += """
    <tr>
        <th colspan='2' style='text-align:center; padding:10px;'>Joint RMSE</th>
    </tr>
    """
    # Add rows for each RMSE value with colored titles
    table_html += f"<tr><td style='color:red;'>X RMSE:</td><td>{rmse_values['x']:.2f}</td></tr>"
    table_html += f"<tr><td style='color:green;'>Y RMSE:</td><td>{rmse_values['y']:.2f}</td></tr>"
    table_html += f"<tr><td style='color:blue;'>Z RMSE:</td><td>{rmse_values['z']:.2f}</td></tr>"
    table_html += '</table>'
    return table_html

def generate_html_report(dataframe_of_3d_data, rmse_dataframe, filename="trajectory_report.html"):
    unique_markers = dataframe_of_3d_data['marker'].unique()

    # Start of the HTML content with included CSS for styling
    html_content = """
    <html>
    <head>
        <title>Trajectory Report</title>
        <style>
            .marker-section {
                border-top: 2px solid #ccc;
                padding-top: 20px;
                margin-top: 20px;
            }
            h1 {
                page-break-before: always; /* Ensures each marker starts on a new page when printed */
            }
            .navigation {
                position: fixed;
                top: 0;
                left: 0;
                background-color: #f8f8f8;
                width: 100%;
                text-align: left;
                padding: 8px 0;
                border-bottom: 1px solid #e7e7e7;
                z-index: 1000;
            }
            .navigation a {
                padding: 6px 12px;
                text-decoration: none;
                color: #007bff;
            }
            .navigation a:hover {
                background-color: #e7e7e7;
            }
            .indicators-container {
                display: flex;
                flex-direction: row;
                align-items: center; /* Center align items horizontally in the column */
                justify-content: center; /* Center align items vertically in the column */
                margin-bottom: 5px; /* Space at the bottom of the container */
            }
            .indicator-wrapper {
                margin: 10px 0; /* Margin around each indicator for spacing */
                width: 10%; /* Full width of the container */
                height: 300px; 
                overflow: hidden; /* Hide content that exceeds the div height */
            }
            table {
                    border-collapse: collapse;
                    width: 200px; /* Set the width of the table */
                    background-color: #f8f8f8; /* Background color */
                    border: 1px solid #ccc; /* Border color */
                    margin-bottom: 10px; /* Space after the table */
                }

            td {
                    padding: 5px; /* Padding inside each cell */
                    text-align: left; /* Align text to the left */
                }

            tr:nth-child(even) {background-color: #f2f2f2;} /* Zebra striping for rows */

            th {
                background-color: #f8f8f8; /* Header background color */
                border-bottom: 1px solid #ccc; /* Border color */
                padding: 5px; /* Padding inside each cell */
                text-align: left; /* Align text to the left */
            }
            }
        </style>

    </head>
    <body>
    <div class='navigation'>
    """

    # Add navigation links
    for marker in unique_markers:
        html_content += f"<a href='#{marker}'>{marker}</a> "

    html_content += "</div>"
    html_content += "<div class='indicators-container'>"
    # html_content += f"<center><h1>Overall RMSE</h1></center>"
    # Add the indicators
    rmse_values = extract_overall_rmse_values_from_dataframe(rmse_dataframe)
    # indicators = create_indicator(rmse_values['total'], "Total RMSE")
    # html_content += fig_to_html(indicators)
    rmse_total_indicator = create_indicator(rmse_values['total'], "Total RMSE")
    rmse_x_indicator = create_indicator(rmse_values['x'], "X RMSE", color_of_text='red', margins_dict = dict(l=1, r=1, b=1, t=1))
    rmse_y_indicator = create_indicator(rmse_values['y'], "Y RMSE", color_of_text='green', margins_dict = dict(l=1, r=1, b=1, t=1))
    rmse_z_indicator = create_indicator(rmse_values['z'], "Z RMSE", color_of_text='blue', margins_dict = dict(l=1, r=1, b=1, t=1))
    indicators = [rmse_total_indicator, rmse_x_indicator, rmse_y_indicator, rmse_z_indicator]
    f = 2
    for indicator in indicators:
        indicator_html = fig_to_html(indicator)
        html_content += f"<div class='indicator-wrapper'>{indicator_html}</div>"

    html_content += "</div>"


    for marker in unique_markers:
        # Add a heading for each marker with an anchor
        html_content += f"<div class='marker-section' id='{marker}'><center><h1>{marker}</h1></center>"



        # Get RMSE values for this marker and generate table
        marker_rmse_values = {
            'x': update_joint_marker_card(marker, rmse_dataframe)[0],
            'y': update_joint_marker_card(marker, rmse_dataframe)[1],
            'z': update_joint_marker_card(marker, rmse_dataframe)[2]
        }
        rmse_table_html = generate_rmse_table(marker_rmse_values)
        html_content += rmse_table_html  # Add the table to the content



        fig_x, fig_y, fig_z = create_joint_trajectory_plots(marker, dataframe_of_3d_data, color_of_cards='white')
        figure = create_subplots_from_individual_figs(fig_x, fig_y, fig_z, color_of_cards='white')
        
        # Convert figures to HTML and add to the report content
        html_content += fig_to_html(figure)
        html_content += "</div>"  # Ends the section for a specific marker

    html_content += "</body></html>"

    with open(filename, "w", encoding='utf-8') as file:
        file.write(html_content)
    print(f"Report saved as {filename}")
