import plotly.express as px

def create_rmse_change_plot(rmse_change_dataframe):
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
                title=f'RMSE Changes',
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

    return fig