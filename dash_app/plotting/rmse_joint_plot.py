import plotly.graph_objects as go

def create_rmse_joint_bar_plot(df):
    dimensions = ['x_error', 'y_error', 'z_error', 'x_velocity_error', 'y_velocity_error', 'z_velocity_error']
    figures = {}
    
    # Calculate the maximum RMSE value across all dimensions
    max_rmse = df['RMSE'].max()
    
    for dim in dimensions:
        filtered_df = df[(df['dimension'] == 'Per Joint') & (df['coordinate'] == dim)]
        fig = go.Figure(data=[
            go.Bar(name=dim, x=filtered_df['marker'], y=filtered_df['RMSE'])
        ])
        fig.update_layout(
            title=f'RMSE for each marker ({dim})',
            xaxis_title='Marker',
            yaxis_title='RMSE Value',
            xaxis=dict(
                tickfont=dict(
                    size=18
                )
            ),
            yaxis=dict(
                range=[0, max_rmse+10]
            )
        )
        figures[dim] = fig
    
    return figures
