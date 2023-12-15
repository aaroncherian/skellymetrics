if __name__ == '__main__':
    from pathlib import Path
    from dash_app.data_utils.load_data import combine_freemocap_and_qualisys_into_dataframe
    from dash_app.data_utils.file_manager import FileManager
    from dash_app.report_generation.html_report_generator import generate_html_report

    path_to_recording_folder = Path(r"D:\2023-05-17_MDN_NIH_data\1.0_recordings\calib_3\sesh_2023-05-17_14_53_48_MDN_NIH_Trial3")

    file_manager = FileManager(path_to_recording_folder)
    freemocap_data = file_manager.freemocap_data
    qualisys_data = file_manager.qualisys_data
    rmse_dataframe = file_manager.rmse_dataframe
    absolute_error_dataframe = file_manager.absolute_error_dataframe
    dataframe_of_3d_data = combine_freemocap_and_qualisys_into_dataframe(freemocap_3d_data=freemocap_data, qualisys_3d_data=qualisys_data)
    html_report = generate_html_report(dataframe_of_3d_data,rmse_dataframe)

    file_name = "trajectory_report.html"
    with open(file_name, "w", encoding='utf-8') as file:
        file.write(html_report)
    print(f"Report saved as {file_name}")
    f = 2