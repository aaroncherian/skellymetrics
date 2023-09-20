import plotly.graph_objects as go


def create_indicator(value, title, color_of_text = 'black'):
    fig = go.Figure(go.Indicator(
        mode="number",
        value=value,
        title={'text': title, 'font': {'color': color_of_text, 'size': 35}}, 
        ))
    fig.update_layout(margin=dict(l=10, r=10, b=10, t=20))
    return fig
