import pandas as pd
import plotly.graph_objs as go


def visualize_shot(series, time_index=None,
                   flow_quantiles=None, weight_quantiles=None, pressure_quantiles=None, title=None):
    series[series < 0] = None

    if time_index is None and isinstance(series.index, pd.TimedeltaIndex):
        time_index = series.index / pd.Timedelta(1, "s")
    else:
        time_index = series.index

    if "espresso_resistance" not in series:
        series["espresso_resistance"] = series["espresso_pressure"] / series["espresso_flow"]

    fig = go.Figure()

    if isinstance(flow_quantiles, (tuple, list)):
        upper = flow_quantiles[1]
        lower = flow_quantiles[0][::-1]
        fig.add_scatter(x=time_index.tolist()+time_index[::-1].tolist(),
                        y=upper.tolist()+ lower.tolist(), mode='lines',
                        opacity=0.3,
                        fill='toself',
                        hoverinfo='none',
                        fillcolor='lightblue',
                        line_color='rgba(255,255,255,0)',
                        name="flow_quantiles")

    if "espresso_flow" in series:
        fig.add_scatter(x=time_index, y=series['espresso_flow'], mode='lines', name="espresso_flow",
                    line={"color": "lightblue"})

    if isinstance(weight_quantiles, (tuple, list)):
        upper = weight_quantiles[1]
        lower = weight_quantiles[0][::-1]
        fig.add_scatter(x=time_index.tolist() + time_index[::-1].tolist(),
                        y=upper.tolist() + lower.tolist(), mode='lines',
                        opacity=0.2,
                        fill='toself',
                        hoverinfo='none',
                        fillcolor='brown',
                        line_color='rgba(255,255,255,0)',
                        name="weight_quantiles")
    if "espresso_flow_weight" in series:
        fig.add_scatter(x=time_index, y=series['espresso_flow_weight'], mode='lines', name="espresso_flow_weight",
                    line={"color": "brown"})

    fig.add_scatter(x=time_index, y=series['espresso_flow_goal'], mode='lines', name="espresso_flow_goal",
                    line={"color": "blue", "dash": "dash"})



    if "espresso_resistance" in series:
        fig.add_scatter(x=time_index, y=series['espresso_resistance'], mode='lines', name="espresso_resistance",
                        line={"color": "yellow"})


    if isinstance(pressure_quantiles, (tuple, list)):
        upper = pressure_quantiles[1]
        lower = pressure_quantiles[0][::-1]
        fig.add_scatter(x=time_index.tolist() + time_index[::-1].tolist(),
                        y=upper.tolist() + lower.tolist(), mode='lines',
                        opacity=0.2,
                        fill='toself',
                        fillcolor='lightgreen',
                        hoverinfo='none',
                        line_color='rgba(255,255,255,0)',
                        name="pressure_quantiles")
    if "espresso_pressure" in series:
        fig.add_scatter(x=time_index, y=series['espresso_pressure'], mode='lines', name="espresso_pressure",
                        line={"color": "lightgreen"})
    fig.add_scatter(x=time_index, y=series['espresso_pressure_goal'], mode='lines', name="espresso_pressure_goal",
                    line={"color": "green", "dash": "dash"})

    fig.update_layout(title=title, hovermode="x", plot_bgcolor="darkgray")
    fig.update_xaxes(title_text='seconds')
    fig.update_yaxes(range=[0, 10])
    return fig
