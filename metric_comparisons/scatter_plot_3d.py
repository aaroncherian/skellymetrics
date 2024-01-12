import plotly.express as px

def create_3d_scatter_from_dataframe(dataframe_of_3d_data, ax_range=1200):
    # Calculate mean values for setting axis ranges
    x_mean = dataframe_of_3d_data["x"].mean()
    y_mean = dataframe_of_3d_data["y"].mean()
    z_mean = dataframe_of_3d_data["z"].mean()

    # Extract unique system names from the dataframe
    system_names = dataframe_of_3d_data['system'].unique()

    # Create a color map for the systems (modify this as needed)
    colors = ['#0b84a5', '#f4bc3d', 'red', 'purple', 'orange', 'yellow']
    color_discrete_map = {system: color for system, color in zip(system_names, colors)}

    # Create the 3D scatter plot
    fig = px.scatter_3d(dataframe_of_3d_data, x="x", y="y", z="z", 
                        animation_frame="frame",
                        animation_group="marker",
                        color="system",
                        color_discrete_map=color_discrete_map,
                        hover_name="marker",
                        hover_data=["x", "y", "z"],
                        range_x=[x_mean - ax_range, x_mean + ax_range], 
                        range_y=[y_mean - ax_range, y_mean + ax_range],
                        range_z=[z_mean - ax_range, z_mean + ax_range]
    )

    # Update the layout of the figure
    fig.update_layout(
        scene_aspectmode='cube',
        autosize=False,
        height=1000,
        width=1100,
        margin={"t": 1, "b": 1, "l": 1, "r": 1},
    )

    # Adjust animation speed
    fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 1000 / 15

    return fig