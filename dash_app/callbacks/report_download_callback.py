from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import io
from dash import dcc

from dash_app.report_generation.html_report_generator import generate_html_report

def register_report_download_callback(app, dataframe_of_3d_data, rmse_dataframe):
    @app.callback(
        Output("download-report", "data"),
        [Input("save-report-btn", "n_clicks")],
        prevent_initial_call=True,
    )
    def generate_and_download_report(n_clicks):
        if n_clicks is None:
            raise PreventUpdate

        # Generate the HTML content for the report
        report_html = generate_html_report(dataframe_of_3d_data, rmse_dataframe)
        # Convert the HTML content to a BytesIO object
        report_io = io.StringIO(report_html)

        # Return the download action
        return dcc.send_string(report_io.getvalue(), "trajectory_report.html")
