import plotly.io as pio
from dash_app.plotting.joint_trajectory_plots import create_joint_trajectory_plots
from plotly.subplots import make_subplots

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

def fig_to_html(fig):
    return pio.to_html(fig, full_html=False)

def generate_html_report(dataframe_of_3d_data, filename="trajectory_report.html"):
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
            }
            .navigation a {
                padding: 6px 12px;
                text-decoration: none;
                color: #007bff;
            }
            .navigation a:hover {
                background-color: #e7e7e7;
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

    for marker in unique_markers:
        # Add a heading for each marker with an anchor
        html_content += f"<div class='marker-section' id='{marker}'><center><h1>{marker}</h1></center>"
        fig_x, fig_y, fig_z = create_joint_trajectory_plots(marker, dataframe_of_3d_data, color_of_cards='white')
        figure = create_subplots_from_individual_figs(fig_x, fig_y, fig_z, color_of_cards='white')
        
        # Convert figures to HTML and add to the report content
        html_content += fig_to_html(figure)
        html_content += "</div>"  # Ends the section for a specific marker

    html_content += "</body></html>"

    with open(filename, "w", encoding='utf-8') as file:
        file.write(html_content)
    print(f"Report saved as {filename}")
