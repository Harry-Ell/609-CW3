'''
plotting code 
'''
import numpy as np
import plotly.graph_objects as go

def surface_plotter(policy, target_score=100, max_turn=100):
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

def plot_isosurface_from_array(array, isovalues=[0.2, 0.4, 0.6, 0.8]):
    array = array[:, :-1, :]
    i_dim, j_dim, k_dim = array.shape
    i, j, k = np.meshgrid(np.arange(i_dim), np.arange(j_dim), np.arange(k_dim), indexing='ij')

    fig = go.Figure()

    # trying to get rid of the value of 0 from the final plots 
   


    for iso_val in isovalues:
        fig.add_trace(go.Isosurface(
            x=i.flatten(),
            y=j.flatten(),
            z=k.flatten(),
            value=array.flatten(),
            isomin=iso_val,
            isomax=iso_val,
            surface_count=1,
            caps=dict(x_show=False, y_show=False, z_show=False),
            opacity=0.5,
            colorscale='Viridis',
            name=f'Iso {iso_val:.2f}'
        ))

    fig.update_layout(
        scene=dict(
            xaxis_title="Player Score",
            yaxis_title="Opponent Score",
            zaxis_title="Turn Total"
        ),
        title="Isosurface Plot of Reachable States",
        margin=dict(l=0, r=0, t=40, b=0)
    )

    fig.show()

