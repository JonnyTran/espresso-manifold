import plotly.graph_objs as go


def visualize_shot(series, time_index):
    series["espresso_resistance"] = series["espresso_pressure"] / series["espresso_flow"]
    series[series < 0] = None

    fig = go.Figure()
    fig.add_scatter(x=time_index, y=series['espresso_flow'], mode='lines', name="espresso_flow",
                    line={"color": "lightblue"})
    fig.add_scatter(x=time_index, y=series['espresso_flow_weight'], mode='lines', name="espresso_flow_weight",
                    line={"color": "brown"})
    fig.add_scatter(x=time_index, y=series['espresso_flow_goal'], mode='lines', name="espresso_flow_goal",
                    line={"dash": "dash"})

    fig.add_scatter(x=time_index, y=series['espresso_resistance'], mode='lines', name="espresso_resistance",
                    line={"color": "yellow"})

    fig.add_scatter(x=time_index, y=series['espresso_pressure'], mode='lines', name="espresso_pressure",
                    line={"color": "teal"})
    fig.add_scatter(x=time_index, y=series['espresso_pressure_goal'], mode='lines', name="espresso_pressure_goal",
                    line={"dash": "dash"})

    fig.update_layout(hovermode="x")
    fig.update_yaxes(range=[0, 10])
    return fig
