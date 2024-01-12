
from pathlib import Path
import pandas as pd
import plotly.express as px

import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt

import numpy as np

from metric_comparison_dash_app.run_dash_app import run_dash_app

def create_3d_scatter_from_dataframe(baseline_system_name, experimental_system_name, dataframe_of_3d_data, ax_range=1200):
    x_mean = dataframe_of_3d_data["x"].mean()
    y_mean = dataframe_of_3d_data["y"].mean()
    z_mean = dataframe_of_3d_data["z"].mean()

    fig = px.scatter_3d(dataframe_of_3d_data, x="x", y="y", z="z", 
                        animation_frame="frame",
                        animation_group="marker",
                        color="system",
                        color_discrete_map={f'{baseline_system_name}': 'blue', f'{experimental_system_name}':'green', 'qualisys': 'red'},
                        hover_name="marker",
                        hover_data=["x", "y", "z"],
                        range_x=[x_mean - ax_range, x_mean + ax_range], 
                        range_y=[y_mean - ax_range, y_mean + ax_range],
                        range_z=[z_mean - ax_range, z_mean + ax_range]
    )
    fig.update_layout(
        scene_aspectmode='cube',
        autosize=False,
        height=1000,
        width=1100,
        margin={"t": 1, "b": 1, "l": 1, "r": 1},
    )

    fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 1000 / 15

    return fig



def load_position_rmse_dataframe(path_to_metrics_folder):
    return pd.read_csv(path_to_metrics_folder / 'position_rmse_dataframe.csv')


def calculate_change_in_rmses(baseline_dataframe, experimental_dataframe):
    rmse_change_dataframe = baseline_dataframe[['marker', 'dimension', 'coordinate']].copy()
    rmse_change_dataframe['rmse_change'] = experimental_dataframe['RMSE'] - baseline_dataframe['RMSE']

    return rmse_change_dataframe


def main(baseline_name, experimental_name):
    baseline_dataframe = load_position_rmse_dataframe(baseline_session_path)
    experimental_dataframe = load_position_rmse_dataframe(experimental_session_path)

    rmse_change_dataframe = calculate_change_in_rmses(baseline_dataframe, experimental_dataframe)

    rmse_change_dataframe = rmse_change_dataframe[rmse_change_dataframe['marker'] != 'All']

    rmse_change_dataframe_for_plotting = rmse_change_dataframe.pivot(index='marker', columns='coordinate', values='rmse_change')
    rmse_change_dataframe_for_plotting.columns = [col.replace('_error', '_change') for col in rmse_change_dataframe_for_plotting.columns]
    rmse_change_dataframe_for_plotting.reset_index(inplace=True)
    rmse_change_dataframe_for_plotting['magnitude'] = rmse_change_dataframe_for_plotting[['x_change', 'y_change', 'z_change']].abs().sum(axis=1)

    f = 2
    

    rmse_change_melted = rmse_change_dataframe_for_plotting.melt(id_vars='marker', value_vars=['x_change', 'y_change', 'z_change'], 
                                         var_name='dimension', value_name='rmse_change')

# Define colors for increase and decrease
    colors = rmse_change_melted['rmse_change'].apply(lambda x: '#EF553B' if x > 0 else '#636EFA')

    # Create grouped bar chart with conditional colors
    fig = px.bar(rmse_change_melted, x='marker', y='rmse_change', color=colors,
                barmode='group', facet_col='dimension',
                title=f'[{experimental_name}] - [{baseline_name}] RMSE Changes',
                color_discrete_map="identity",
                template='seaborn')  # Use the actual color values in 'colors'


    # Update layout for clarity
    fig.update_layout(showlegend=False)
    fig.update_xaxes(title_text='Joint')
    fig.update_yaxes(title_text='Change in RMSE (mm)', row=1, col=1)

    # Ensure that other y-axes do not repeat the label
    # fig.update_yaxes(title_text='', matches=None, showticklabels=True, row=1, col=2)
    # fig.update_yaxes(title_text='', matches=None, showticklabels=True, row=1, col=3)
        

    titles = ['RMSE Change Across X Dimension', 'RMSE Change Across Y Dimension', 'RMSE Change Across Z Dimension']

    # Assuming there are three facets for the x_change, y_change, and z_change
    for i, title in enumerate(titles):
        fig.layout.annotations[i]['text'] = title  # Update the text of each annotation
        fig.layout.annotations[i]['font'] = dict(size=18)  # Update the font size as needed


    # Show the plot
    fig.show()

    print(rmse_change_dataframe)


session_path = Path(r'D:\2023-06-07_TF01\1.0_recordings\treadmill_calib\sesh_2023-06-07_12_06_15_TF01_flexion_neutral_trial_1')
# session_path = Path(r"D:\2023-05-17_MDN_NIH_data\1.0_recordings\calib_3\sesh_2023-05-17_13_48_44_MDN_treadmill_2")

baseline_session = 'mediapipe_dlc'
experimental_session = 'mediapipe_yolo_dlc'

baseline_session_path = session_path/'metrics'/f'{baseline_session}_metrics'
experimental_session_path = session_path/'metrics'/f'{experimental_session}_metrics'

baseline_data = pd.read_csv(session_path/'metrics'/f'{baseline_session}_freemocap_position_data.csv')
baseline_data['system'] = baseline_data['system'].replace({'freemocap':f'{baseline_session}'})

experimental_data = pd.read_csv(session_path/'metrics'/f'{experimental_session}_freemocap_position_data.csv')
experimental_data['system'] = experimental_data['system'].replace({'freemocap':f'{experimental_session}'})

qualisys_data = pd.read_csv(session_path/'metrics'/'qualisys_position_data.csv')

position_dataframe = pd.concat([baseline_data, experimental_data,qualisys_data], ignore_index=True)


run_dash_app(position_dataframe)
# fig = create_3d_scatter_from_dataframe(baseline_session, experimental_session, position_dataframe)

# fig.show()

f=2




# main(baseline_name=baseline_session, experimental_name=experimental_session)
