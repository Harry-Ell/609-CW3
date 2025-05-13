'''
plotting code 
'''
import numpy as np
import plotly.graph_objects as go

def plotter(policy, target_score=100, max_turn=100):
    xs, ys, zs = [], [], []

    for ps in range(target_score):
        for os in range(target_score):
            for t in range(max_turn + 1):
                if policy[ps, os, t] == 1:  # 1 = roll
                    xs.append(ps)
                    ys.append(os)
                    zs.append(t)  # Record the turn total at which the decision is "roll"

    fig = go.Figure(data=[go.Scatter3d(
        x=xs,
        y=ys,
        z=zs,
        mode='markers',
        marker=dict(
            size=3,
            color=zs,  # Color based on turn total
            colorscale='RdYlGn',  # Perceptually uniform and colorblind-friendly
            opacity=0.7,
            colorbar=dict(title='Turn Total')  # Adds a colorbar legend
        )
    )])

    fig.update_layout(
        scene=dict(
            xaxis_title='Player Score',
            yaxis_title='Opponent Score',
            zaxis_title='Turn Total',
        ),
        title="Decision Points Where Action is 'Roll'",
        width=900,
        height=750
    )

    fig.show()

