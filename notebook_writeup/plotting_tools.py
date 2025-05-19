'''
plotting code
'''
import numpy as np
import plotly.graph_objects as go


def plot_isosurface_from_array(array, isovalues=[0.2, 0.4, 0.6, 0.8], save_as=None, perspective = [1,1,1]):
    # Drop the last slice as before
    array = array[:, :-1, :]
    i_dim, j_dim, k_dim = array.shape
    i, j, k = np.meshgrid(
        np.arange(i_dim), np.arange(j_dim), np.arange(k_dim),
        indexing='ij'
    )

    fig = go.Figure()

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
            opacity=0.8,
            colorscale='Viridis',
            showscale=False,            # hide the colorbar
            name=f'Iso {iso_val:.2f}'
        ))

    # Update layout with grid in the background
    fig.update_layout(
        font=dict(family='serif'),
        title=dict(
            text='Contours of Equal Win Probability',
            x=0.5,
            y=0.75,
            xanchor='center',
            font=dict(size=20, family='serif')
        ),
        scene=dict(
            xaxis=dict(
                title=dict(text='Player Score', font=dict(family='serif')),
                tickfont=dict(family='serif'),
                showgrid=True,                # enable grid lines
                gridcolor='lightgrey',        # grid line color
                showbackground=True,          # show background plane
                backgroundcolor='rgba(240,240,240,0.5)'  # light background
            ),
            yaxis=dict(
                title=dict(text='Opponent Score', font=dict(family='serif')),
                tickfont=dict(family='serif'),
                showgrid=True,
                gridcolor='lightgrey',
                showbackground=True,
                backgroundcolor='rgba(240,240,240,0.5)'
            ),
            zaxis=dict(
                title=dict(text='Turn Total', font=dict(family='serif')),
                tickfont=dict(family='serif'),
                showgrid=True,
                gridcolor='lightgrey',
                showbackground=True,
                backgroundcolor='rgba(240,240,240,0.5)'
            )
        ), scene_camera=dict(eye=dict(x=perspective[0], y=perspective[1], z=perspective[2]))
    )
    if save_as:
        fig.write_image(save_as, scale = 3)
    fig.show()


def generate_box_plots(array, title = 'Isosurface Plot of Reachable States', pad = False, save_as=None, perspective = [1,1,1]):
    if pad == True:
        padded = np.pad(array,
                        pad_width=1,
                        mode='constant',
                        constant_values=0)
    else: 
        padded = array

    i_dim, j_dim, k_dim = padded.shape
    i, j, k = np.meshgrid(
        np.arange(i_dim), np.arange(j_dim), np.arange(k_dim),
        indexing='ij'
    )

    fig = go.Figure(data = go.Isosurface(
        x=i.flatten(),
        y=j.flatten(),
        z=k.flatten(),
        value=padded.flatten(),
        isomin=0.75,
        isomax=1.0,
        surface_count=1,
        caps=dict(x_show=False, y_show=False, z_show=False),
        opacity=1,
        colorscale=[(0, 'darkgray'), (1, 'gray')],
        showscale=False,            # hide the colorbar
    ))

    # Update layout with grid in the background
    fig.update_layout(
        font=dict(family='serif'),
        title=dict(
            text=title,
            x=0.5,
            y=0.75,
            xanchor='center',
            font=dict(size=20, family='serif')
        ),
        scene=dict(
            xaxis=dict(
                title=dict(text='Player Score', font=dict(family='serif')),
                tickfont=dict(family='serif'),
                showgrid=True,                # enable grid lines
                gridcolor='lightgrey',        # grid line color
                showbackground=True,          # show background plane
                backgroundcolor='rgba(240,240,240,0.5)'  # light background
            ),
            yaxis=dict(
                title=dict(text='Opponent Score', font=dict(family='serif')),
                tickfont=dict(family='serif'),
                showgrid=True,
                gridcolor='lightgrey',
                showbackground=True,
                backgroundcolor='rgba(240,240,240,0.5)'
            ),
            zaxis=dict(
                title=dict(text='Turn Total', font=dict(family='serif')),
                tickfont=dict(family='serif'),
                showgrid=True,
                gridcolor='lightgrey',
                showbackground=True,
                backgroundcolor='rgba(240,240,240,0.5)'
            )
        ), scene_camera=dict(eye=dict(x=perspective[0], y=perspective[1], z=perspective[2]))
    )
    if save_as:
        fig.write_image(save_as, scale = 3)
    fig.show()