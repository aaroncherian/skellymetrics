
from pathlib import Path
import pandas as pd
import plotly.express as px

import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt

def load_position_rmse_dataframe(path_to_metrics_folder):
    return pd.read_csv(path_to_metrics_folder / 'position_rmse_dataframe.csv')


def calculate_change_in_rmses(rmse_dataframe_one, rmse_dataframe_two):
    rmse_change_dataframe = rmse_dataframe_one[['marker', 'dimension', 'coordinate']].copy()
    rmse_change_dataframe['rmse_change'] = rmse_dataframe_one['RMSE'] - rmse_dataframe_two['RMSE']

    return rmse_change_dataframe


def main():
    rmse_dataframe_one = load_position_rmse_dataframe(metric_one_path)
    rmse_dataframe_two = load_position_rmse_dataframe(metric_two_path)

    rmse_change_dataframe = calculate_change_in_rmses(rmse_dataframe_one, rmse_dataframe_two)

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
                title='[Mediapipe/Yolo with REF + DLC] - [Mediapipe + DLC] RMSE Changes',
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

metric_one_path = session_path/'output_data'/'mediapipe_dlc_metrics'
metric_two_path = session_path/'output_data'/'mediapipe_yolo_dlc_metrics'

main()
