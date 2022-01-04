import pandas as pd
import plotly.graph_objs as go


def visualize_shot(shot, time_index=None,
                   flow_quantiles=None, weight_quantiles=None, pressure_quantiles=None, title=None,
                   weight_col='espresso_flow_weight', resistance_col="espresso_resistance",
                   pressure_col="espresso_pressure", flow_col="espresso_flow"):
    if isinstance(shot.index, pd.MultiIndex):
        shot.index = shot.index.get_level_values(-1)

    shot.replace({-1: None}, inplace=True)

    if time_index is None and isinstance(shot.index, pd.TimedeltaIndex):
        time_index = shot.index / pd.Timedelta(1, "s")
    else:
        time_index = shot.index

    fig = go.Figure()

    # Flow
    if isinstance(flow_quantiles, (tuple, list)):
        upper = flow_quantiles[1]
        lower = flow_quantiles[0][::-1]
        fig.add_scatter(x=time_index.tolist() + time_index[::-1].tolist(),
                        y=upper.tolist() + lower.tolist(), mode='lines',
                        opacity=0.3,
                        fill='toself',
                        hoverinfo='none',
                        fillcolor='lightblue',
                        line_color='rgba(255,255,255,0)',
                        name="flow_quantiles")

    if flow_col in shot:
        fig.add_scatter(x=time_index, y=shot[flow_col], mode='lines', name=flow_col,
                        line={"color": "lightblue"})

    # Flow
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
    if weight_col in shot:
        fig.add_scatter(x=time_index, y=shot[weight_col], mode='lines', name=weight_col,
                        line={"color": "brown"})

    fig.add_scatter(x=time_index, y=shot['espresso_flow_goal'], mode='lines', name="espresso_flow_goal",
                    line={"color": "blue", "dash": "dash"})

    # Resistance
    # if "espresso_resistance" not in shot:
    #     shot["espresso_resistance"] = shot["espresso_pressure"] / shot["espresso_flow"]
    if resistance_col in shot:
        fig.add_scatter(x=time_index, y=shot[resistance_col], mode='lines', name=resistance_col,
                        line={"color": "yellow"})

    # Pressure
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
    if pressure_col in shot:
        fig.add_scatter(x=time_index, y=shot[pressure_col], mode='lines', name=pressure_col,
                        line={"color": "lightgreen"})

    fig.add_scatter(x=time_index, y=shot['espresso_pressure_goal'], mode='lines', name="espresso_pressure_goal",
                    line={"color": "green", "dash": "dash"})

    # State change
    if 'espresso_state_change' in shot:
        for i, val in zip(time_index, shot["espresso_state_change"]):
            if val is None: continue
            if val == 0.0 or val == "0.0":
                fig.add_vline(x=i, line_width=1, line_dash="dash", line_color="black", name='espresso_state_change')
            # else:sadd_vline(x=i, line_width=1, line_dash="dash", line_color="orange", name='espresso_state_change')

    fig.update_layout(title=title, hovermode="x", plot_bgcolor="darkgray")
    fig.update_xaxes(title_text='seconds', showgrid=False)
    fig.update_yaxes(range=[0, 10], showgrid=True)
    return fig
