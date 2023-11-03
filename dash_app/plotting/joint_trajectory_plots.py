import plotly.express as px
from dash import dcc


def create_joint_trajectory_plots(marker, dataframe_of_3d_data, color_of_cards):
    df_marker = dataframe_of_3d_data[dataframe_of_3d_data.marker == marker]
    
    trajectory_plot_height = 350
    # Your plotting code here. For demonstration, using placeholders.
    fig_x = px.line(df_marker, x='frame', y='x', color='system', color_discrete_map={'freemocap': 'blue', 'qualisys': 'red'}, render_mode='svg')
    fig_y = px.line(df_marker, x='frame', y='y', color='system', color_discrete_map={'freemocap': 'blue', 'qualisys': 'red'}, render_mode='svg')
    fig_z = px.line(df_marker, x='frame', y='z', color='system', color_discrete_map={'freemocap': 'blue', 'qualisys': 'red'}, render_mode='svg')
    fig_x_vel = px.line(df_marker, x='frame', y='x_velocity', color='system', color_discrete_map={'freemocap': 'blue', 'qualisys': 'red'}, render_mode='svg')
    fig_y_vel = px.line(df_marker, x='frame', y='y_velocity', color='system', color_discrete_map={'freemocap': 'blue', 'qualisys': 'red'}, render_mode='svg')
    fig_z_vel = px.line(df_marker, x='frame', y='z_velocity', color='system', color_discrete_map={'freemocap': 'blue', 'qualisys': 'red'}, render_mode='svg')

    fig_x.update_xaxes(title_text='', showticklabels=False)
    fig_x.update_yaxes(title_text='X', title_font=dict(size=18))
    fig_x.update_layout(paper_bgcolor=color_of_cards)

    fig_y.update_xaxes(title_text='', showticklabels=False)
    fig_y.update_yaxes(title_text='Y', title_font=dict(size=18))
    fig_y.update_layout(paper_bgcolor=color_of_cards, height=trajectory_plot_height)

    fig_z.update_xaxes(title_text='Frame', title_font=dict(size=18))
    fig_z.update_yaxes(title_text='Z', title_font=dict(size=18))
    fig_z.update_layout(paper_bgcolor=color_of_cards, height=trajectory_plot_height)

    fig_x_vel.update_xaxes(title_text='', showticklabels=False)
    fig_x_vel.update_yaxes(title_text='X Velocity', title_font=dict(size=18))
    fig_x_vel.update_layout(paper_bgcolor=color_of_cards)

    fig_y_vel.update_xaxes(title_text='', showticklabels=False)
    fig_y_vel.update_yaxes(title_text='Y Velocity', title_font=dict(size=18))
    fig_y_vel.update_layout(paper_bgcolor=color_of_cards, height=trajectory_plot_height)

    fig_z_vel.update_xaxes(title_text='Frame', title_font=dict(size=18))
    fig_z_vel.update_yaxes(title_text='Z Velocity', title_font=dict(size=18))
    fig_z_vel.update_layout(paper_bgcolor=color_of_cards, height=trajectory_plot_height)

    # Return the list of Plotly figures
    return [dcc.Graph(figure=fig_x), dcc.Graph(figure=fig_y), dcc.Graph(figure=fig_z), dcc.Graph(figure=fig_x_vel), dcc.Graph(figure=fig_y_vel), dcc.Graph(figure=fig_z_vel)]
